import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertModel, DistilBertTokenizer, AdamW
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from thop import profile, clever_format
from pyJoules.energy_meter import measure_energy
from pyJoules.device.rapl_device import RaplPackageDomain, RaplCoreDomain
import time
import sys
import os
import csv

assert sys.version_info.major == 3 and sys.version_info.minor == 8, "This script requires Python 3.8"

print(sys.executable)
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.version.cuda)

# Check if CUDA is available
is_cuda_available = torch.cuda.is_available()

device = torch.device("cuda" if is_cuda_available else "cpu")
print('Running on', device)

# Load and preprocess the dataset
df = pd.read_csv("question_answer_pairs.txt", delimiter='\t')
print(df.head())

# Define the LabelEncoder
le = LabelEncoder()
df['encoded_answers'] = le.fit_transform(df['Answer'])

# Define a PyTorch Dataset
class QnADataset(Dataset):
    def __init__(self, questions, answers, tokenizer, max_length):
        self.questions = questions
        self.answers = answers
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.questions)

    def __getitem__(self, idx):
        question = str(self.questions[idx])
        encoding = self.tokenizer.encode_plus(
            question,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
            truncation=True
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'answers': torch.tensor(self.answers[idx], dtype=torch.long)
        }

# Define the model
class QnAModel(nn.Module):
    def __init__(self, n_classes):
        super(QnAModel, self).__init__()
        self.bert = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):
        output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = output.last_hidden_state 
        pooled_output = last_hidden_state.mean(dim=1) 
        output = self.drop(pooled_output)
        return self.out(output)

# Initialize the DataLoader
def create_data_loader(df, tokenizer, max_length, batch_size):
    ds = QnADataset(
        questions=df.Question.to_numpy(),
        answers=df.encoded_answers.to_numpy(),
        tokenizer=tokenizer,
        max_length=max_length
    )
    return DataLoader(ds, batch_size=batch_size)

# Count unique answers
n_classes = len(le.classes_)
model = QnAModel(n_classes)
model = model.to(device)

# Initialize tokenizer, model, and data loaders
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
net = QnAModel(n_classes).to(device)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

BATCH_SIZE = 16
MAX_LEN = 128
train_data_loader = create_data_loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE)
val_data_loader = create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)
test_loader = create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)

print("Number of batches in train_data_loader:", len(train_data_loader))
print("Number of batches in val_data_loader:", len(val_data_loader))

# Function to log energy to CSV
def log_energy_to_csv(tag, begin_timestamp, duration, package_0, core_0):
    with open('energy_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([tag, begin_timestamp, duration, package_0, core_0])

# Define the test function
def test(net, test_loader):
    net.eval()
    total_correct = 0
    total_count = 0
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            answers = batch['answers'].to(device)
            outputs = net(input_ids, attention_mask)
            _, predicted = torch.max(outputs, dim=1)
            total_correct += (predicted == answers).sum().item()
            total_count += answers.size(0)
    return total_correct / total_count

if __name__ == "__main__":
    test_acc = test(net, test_loader)
    print('Test Accuracy:', test_acc)

# Profile the model
dummy_input_ids = torch.randint(0, tokenizer.vocab_size, (1, MAX_LEN)).to(device)
dummy_attention_mask = torch.ones(1, MAX_LEN).to(device)
macs, params = profile(model, inputs=(dummy_input_ids, dummy_attention_mask))

macs, params = clever_format([macs, params], "%.3f")
print(f"MACs (Multiply-Accumulate operations): {macs}")
print(f"Parameters: {params}")

# Training loop
EPOCHS = 1
optimizer = AdamW(model.parameters(), lr=3e-5)

def get_accuracy(preds, labels):
    _, predictions = torch.max(preds, dim=1)
    correct = (predictions == labels).sum().float()
    total = labels.shape[0]
    return correct / total

@measure_energy(domains=[RaplPackageDomain(0), RaplCoreDomain(0)])
def train_one_epoch(epoch, model, data_loader, optimizer, device):
    model.train()
    for i, data in enumerate(data_loader, 0):
        start_time = time.time()
        input_ids = data['input_ids'].to(device)
        attention_mask = data['attention_mask'].to(device)
        answers = data['answers'].to(device)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        _, preds = torch.max(outputs, dim=1)
        loss = nn.CrossEntropyLoss()(outputs, answers)
        acc = get_accuracy(outputs, answers)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        end_time = time.time()
        training_time = end_time - start_time
        print(f'Epoch: {epoch}, Batch: {i}, Training time: {training_time} seconds, Loss: {loss.item()}, Accuracy: {acc.item()}')
        log_energy_to_csv('train_one_epoch', start_time, training_time, RaplPackageDomain(0), RaplCoreDomain(0))

@measure_energy(domains=[RaplPackageDomain(0), RaplCoreDomain(0)])
def evaluate(epoch, model, data_loader, device):
    model.eval()
    val_accs = []
    with torch.no_grad():
        for i, data in enumerate(data_loader, 0):
            start_time = time.time()
            input_ids = data['input_ids'].to(device)
            attention_mask = data['attention_mask'].to(device)
            answers = data['answers'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            acc = get_accuracy(outputs, answers)
            val_accs.append(acc.item())

            end_time = time.time()
            simulation_time = end_time - start_time
            print(f'Validation Epoch: {epoch}, Batch: {i}, Simulation time: {simulation_time} seconds')
            log_energy_to_csv('evaluate', start_time, simulation_time, RaplPackageDomain(0), RaplCoreDomain(0))

        val_acc = sum(val_accs) / len(val_accs)
        print(f'Validation accuracy after epoch {epoch}: {val_acc}')

for epoch in range(EPOCHS):
    train_one_epoch(epoch, model, train_data_loader, optimizer, device)
    evaluate(epoch, model, val_data_loader, device)

