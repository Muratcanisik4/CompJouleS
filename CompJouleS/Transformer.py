import time
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertModel, DistilBertTokenizer, AdamW
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from thop import profile, clever_format



#device = torch.device("cpu")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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

# Initialize the tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Initialize the DataLoader
def create_data_loader(df, tokenizer, max_length, batch_size):
    ds = QnADataset(
        questions=df.Question.to_numpy(),
        answers=df.encoded_answers.to_numpy(),
        tokenizer=tokenizer,
        max_length=max_length
    )
    return DataLoader(ds, batch_size=batch_size)

BATCH_SIZE = 16
MAX_LEN = 128
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
train_data_loader = create_data_loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE)
val_data_loader = create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)

print("Number of batches in train_data_loader:", len(train_data_loader))
print("Number of batches in val_data_loader:", len(val_data_loader))



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

# Count unique answers
n_classes = len(le.classes_)

model = QnAModel(n_classes)
model = model.to(device)




dummy_input_ids = torch.randint(0, tokenizer.vocab_size, (1, MAX_LEN)).to(device)
dummy_attention_mask = torch.ones(1, MAX_LEN).to(device)
macs, params = profile(model, inputs=(dummy_input_ids, dummy_attention_mask))



# Format the output for better readability
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

for epoch in range(EPOCHS):
    model.train()
    for i, data in enumerate(train_data_loader, 0):
        start_time = time.time() # Start the timer
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

        end_time = time.time() # End the timer
        training_time = end_time - start_time # Calculate training time
        print(f'Epoch: {epoch}, Batch: {i}, Training time: {training_time} seconds')

    model.eval()
    with torch.no_grad():
        val_accs = []
        for i, data in enumerate(val_data_loader, 0):
            start_time = time.time() # Start the timer
            input_ids = data['input_ids'].to(device)
            attention_mask = data['attention_mask'].to(device)
            answers = data['answers'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            acc = get_accuracy(outputs, answers) 
            val_accs.append(acc.item())

            end_time = time.time() # End the timer
            simulation_time = end_time - start_time # Calculate simulation time
            print(f'Validation Epoch: {epoch}, Batch: {i}, Simulation time: {simulation_time} seconds')

        val_acc = sum(val_accs) / len(val_accs)
        print(f'Validation accuracy after epoch {epoch}: {val_acc}')





#print(f"MACs: {macs}")
#print(f"Parameters: {params}")






