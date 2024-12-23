from utils import *
from parameters import *
from parameters_opt import *
# import deephyper
from pyJoules.energy_meter import measure_energy
from pyJoules.device.rapl_device import RaplPackageDomain
from pyJoules.device.nvidia_device import NvidiaGPUDomain
from pyJoules.device.rapl_device import RaplCoreDomain
import numpy as np

# Network variables

train_acc = np.zeros((sim_dict['maxE']))
test_acc = np.zeros_like(train_acc)
n_train = sim_dict['n_train']
n_test = sim_dict['n_test']
spike_count = 0.0
spike_count_hidden_avg = 0.0
# print (network_arch_dict['n_h1'], paramdict['n_h1'],"size outside loop")

def get_weights(paramdict):
    sim_dict.update(paramdict)
    lr_paramdict.update(paramdict)
    network_arch_dict.update(paramdict)
    sim_dict.update({'nBins': int(np.floor(sim_dict['tSim'] / sim_dict['dt_conv']))})
    w_in, w_out, w_err_h1p, w_err_h1n = init_weights(network_arch_dict, lr_paramdict)
    TrainIm, TrainLabels, TestIm, TestLabels = mnist_dataloader('.\data\MNIST\\raw', sim_dict['n_train'],
                                                        sim_dict['n_test'])
    return w_in, w_out, w_err_h1p, w_err_h1n, TrainIm, TrainLabels, TestIm, TestLabels

# Trainer model
#@measure_energy(domains=[RaplPackageDomain(0), NvidiaGPUDomain(0)])
def trainer_func(param_config, w_in, w_out, w_err_h1p, w_err_h1n, TrainIm, TrainLabels, TestIm, TestLabels, test_flag=0):
    sim_dict.update(param_config)
    lr_paramdict.update(param_config)
    sim_dict.update({'nBins': int(np.floor(sim_dict['tSim'] / sim_dict['dt_conv']))})
    network_arch_dict.update(param_config)


    # train_acc = np.zeros((sim_dict['maxE']))
    # test_acc = np.zeros_like(train_acc)
    # n_train = sim_dict['n_train']
    # n_test = sim_dict['n_test']
    # spike_count = 0.0
    # spike_count_hidden_avg = 0.0

    # print (f'The hidden layer size inside loop is {network_arch_dict["n_h1"]}')
    for e in range(sim_dict['maxE']):  # for each epoch
        correct_predictions = 0
        test_predictions = 0
        if test_flag== 0:
            for u in range(sim_dict['n_train']):  # for each training pattern
                # Generate poisson data and labels
                spikeMat = MNIST_to_Spikes(sim_dict['MaxF'], TrainIm[u], sim_dict['tSim'], sim_dict['dt_conv'])
                fr_label = np.zeros(network_arch_dict['n_out'])
                fr_label[TrainLabels[u]] = sim_dict['maxFL']  # target output spiking frequencies
                s_label = make_spike_trains(fr_label * sim_dict['dt_conv'], sim_dict['nBins'])  # target spikes

                # Initialize hidden layer variables
                I1 = np.zeros(network_arch_dict['n_h1'])
                V1 = np.zeros(network_arch_dict['n_h1'])
                U1 = np.zeros(network_arch_dict['n_h1'])

                # Initialize output layer variables
                I2 = np.zeros(network_arch_dict['n_out'])
                V2 = np.zeros(network_arch_dict['n_out'])
                U2 = np.zeros(network_arch_dict['n_out'])

                # Initialize error neuron variables
                Verr1 = np.zeros(network_arch_dict['n_out'])
                Verr2 = np.zeros(network_arch_dict['n_out'])

                # Initialize firing time variables
                ts1 = np.full(network_arch_dict['n_h1'], -1 * neuron_paramdict['t_refr'])
                ts2 = np.full(network_arch_dict['n_out'], -1 * neuron_paramdict['t_refr'])
                tsE1 = np.full(network_arch_dict['n_out'], -1 * neuron_paramdict['t_refr'])
                tsE2 = np.full(network_arch_dict['n_out'], -1 * neuron_paramdict['t_refr'])

                SE1T = np.zeros((10, sim_dict['nBins']))  # to record error neuron spiking
                SE2T = np.zeros((10, sim_dict['nBins']))
                train_counter = np.zeros((network_arch_dict['n_out']))
                for t in range(sim_dict['nBins']):  # for the number of time steps
                    # Forward pass

                    # Find input neurons that spike
                    fired_in = np.nonzero(spikeMat[:, t])
                    # print (len(fired_in))
                    # Update synaptic current into hidden layer
                    # print (w_in.shape, I1.shape, spikeMat[:,t].shape, "The shape of w_in")
                    I1 = I1 + (sim_dict['dt'] / neuron_paramdict['t_syn']) * (w_in.dot(spikeMat[:, t]) - I1)

                    # Update hidden layer membrane potentials
                    V1 = V1 + (sim_dict['dt'] / neuron_paramdict['t_m']) * (
                            (neuron_paramdict['V_rest'] - V1) + I1 * neuron_paramdict['R'])
                    V1[V1 < -neuron_paramdict['Vth'] / 10] = -neuron_paramdict['Vth'] / 10  # Limit negative potential

                    # If neuron in refractory period, prevent changes to membrane potential
                    refr1 = (t * sim_dict['dt'] - ts1 <= neuron_paramdict['t_refr'])
                    V1[refr1] = 0

                    fired = np.nonzero(V1 >= neuron_paramdict['Vth'])  # Hidden neurons that spiked
                    V1[fired] = 0  # Reset their membrane potential to zero
                    ts1[fired] = t  # Update their most recent spike times

                    ST1 = np.zeros(network_arch_dict['n_h1'])  # Hidden layer spiking activity
                    ST1[fired] = 1  # Set neurons that spiked to 1

                    # Repeat the process for the output layer
                    I2 = I2 + (sim_dict['dt'] / neuron_paramdict['t_syn1']) * (w_out.dot(ST1) - I2)

                    V2 = V2 + (sim_dict['dt'] / neuron_paramdict['t_mH']) * (
                            (neuron_paramdict['V_rest'] - V2) + I2 * (neuron_paramdict['RH']))
                    V2[V2 < -neuron_paramdict['VthO'] / 10] = -neuron_paramdict['VthO'] / 10

                    refr2 = (t * sim_dict['dt'] - ts2 <= neuron_paramdict['t_refr'])
                    V2[refr2] = 0
                    fired2 = np.nonzero(V2 >= neuron_paramdict['VthO'])
                    V2[fired2] = 0
                    ts2[fired2] = t

                    s2 = np.zeros((network_arch_dict['n_out']))
                    s2[fired2] = 1
                    train_counter = train_counter + s2
                    # Compute error (used as input to error neurons)
                    Ierr = s2 - s_label[:, t]
                    Ierr = Ierr.reshape((Ierr.shape[0]))
                    # Update error neurons and check for firing (positive and negative error neurons)
                    # If an error neuron fires, it spikes and has it membrane
                    # potential decreased by VthE

                    # Compute the False Positive neuron update
                    Verr1 = Verr1 + (sim_dict['dt'] * neuron_paramdict['RE'] / neuron_paramdict['t_mE']) * (Ierr)
                    Verr1[TrainLabels[u]] = 0  # Setting the target label to 0 since it is not FP
                    # Set the Verr from falling below the threshold and falling too negative
                    Verr1[Verr1 < -neuron_paramdict['VthE'] / 10] = -neuron_paramdict['VthE'] / 10
                    # Find the fired error neurons
                    fired_err = (Verr1 >= neuron_paramdict['VthE'])
                    Verr1[fired_err] -= neuron_paramdict['VthE']
                    # Note their indexes and time of fire
                    sE1 = np.zeros((network_arch_dict['n_out']))
                    sE1[fired_err] = 1
                    tsE1[fired_err] = t

                    # Compute the False Negative neuron update
                    Verr2 = Verr2 + (sim_dict['dt'] * neuron_paramdict['RE'] / neuron_paramdict['t_mE']) * (-Ierr)

                    # Set the Verr from falling below the threshold and falling too negative
                    Verr2[Verr2 < -neuron_paramdict['VthE'] / 10] = -neuron_paramdict['VthE'] / 10

                    # Find the fired error neurons
                    fired_err = (Verr2 >= neuron_paramdict['VthE'])
                    Verr2[fired_err] -= neuron_paramdict['VthE']
                    # Note their indexes and time of fire
                    sE2 = np.zeros((network_arch_dict['n_out']))
                    sE2[fired_err] = 1
                    tsE2[fired_err] = t
                    # print(sE1.shape, w_err_h1p.shape, U1.shape)
                    # Update second compartment (U1/U2) with error feedback
                    U1 = U1 + (sim_dict['dt'] / neuron_paramdict['t_mU']) * (-U1 + (
                            lr_paramdict['lrP'] * np.matmul(w_err_h1p, sE1) - lr_paramdict['lrN'] * np.matmul(w_err_h1n,
                                                                                                              sE2)) *
                                                                             neuron_paramdict['RU'])
                    U2 = U2 + (sim_dict['dt'] / neuron_paramdict['t_mU']) * (-U2 + (sE1 - sE2) * neuron_paramdict['RU'])
                    # Compute hidden layer weight updates
                    # Check if input neurons fired
                    # Check if hidden neuron current (I1) is between Imin and Imax
                    # Update weights (w_in) based on learning rate (lr0) and error (U1)

                    for hidden_neuron in range(network_arch_dict['n_h1']):
                        if (lr_paramdict['Imin'] <= I1[hidden_neuron] and I1[hidden_neuron] <= lr_paramdict['Imax']):
                            w_in[hidden_neuron, fired_in] -= lr_paramdict['lr0'] * U1[hidden_neuron]

                    # Compute output layer weight updates
                    # Check if hidden neurons fired
                    # Check if output neuron current (I2) is between Imin and Imax
                    # Update weights (w_out) based on learning rate (lr1) and error (U2)

                    for output_neuron in range(network_arch_dict['n_out']):
                        if (lr_paramdict['Imin'] <= I2[output_neuron] and I2[output_neuron] <= lr_paramdict['Imax']):
                            w_out[output_neuron, fired] -= lr_paramdict['lr1'] * U2[output_neuron]

                # Check train and test accuracy here.
                # If the output neuron with highest firing rate matches the target
                # neuron, and that rate is > 0, then the sample was classified correctly
                tn = TrainLabels[u]
                wn = np.argmax(train_counter)
                # print (train_counter, wn, tn)
                if tn == wn:
                    correct_predictions += 1
    print(correct_predictions)

    # print(f'Accuracy in epoch {e} is {(correct_predictions / n_train)} {correct_predictions}')
    # train_acc[e] = (correct_predictions / sim_dict['n_train']) * 100
    if test_flag==1:
    ## Perform Testing
        for u in range(sim_dict['n_test']):  # for each training pattern
            # Generate poisson data and labels
            spikeMat = MNIST_to_Spikes(sim_dict['MaxF'], TestIm[u], sim_dict['tSim'], sim_dict['dt_conv'])
            fr_label = np.zeros(network_arch_dict['n_out'])
            fr_label[TestLabels[u]] = sim_dict['maxFL']  # target output spiking frequencies
            s_label = make_spike_trains(fr_label * sim_dict['dt_conv'], sim_dict['nBins'])  # target spikes
            # print (f'{network_arch_dict["n_h1"]}, values')
            # Initialize hidden layer variables
            I1 = np.zeros(network_arch_dict['n_h1'])
            V1 = np.zeros(network_arch_dict['n_h1'])
            U1 = np.zeros(network_arch_dict['n_h1'])

            # Initialize output layer variables
            I2 = np.zeros(network_arch_dict['n_out'])
            V2 = np.zeros(network_arch_dict['n_out'])
            U2 = np.zeros(network_arch_dict['n_out'])

            # Initialize error neuron variables
            Verr1 = np.zeros(network_arch_dict['n_out'])
            Verr2 = np.zeros(network_arch_dict['n_out'])

            # Initialize firing time variables
            ts1 = np.full(network_arch_dict['n_h1'], -neuron_paramdict['t_refr'])
            ts2 = np.full(network_arch_dict['n_out'], -neuron_paramdict['t_refr'])
            tsE1 = np.full(network_arch_dict['n_out'], -neuron_paramdict['t_refr'])
            tsE2 = np.full(network_arch_dict['n_out'], -neuron_paramdict['t_refr'])

            SE1T = np.zeros((10, sim_dict['nBins']))  # to record error neuron spiking
            SE2T = np.zeros((10, sim_dict['nBins']))
            test_counter = np.zeros((network_arch_dict['n_out']))

            for t in range(sim_dict['nBins']):
                # Forward pass

                # Find input neurons that spike
                fired_in = np.nonzero(spikeMat[:, t])
                # print (len(fired_in))
                # Update synaptic current into hidden layer
                I1 = I1 + (sim_dict['dt'] / neuron_paramdict['t_syn']) * (w_in.dot(spikeMat[:, t]) - I1)

                # Update hidden layer membrane potentials
                V1 = V1 + (sim_dict['dt'] / neuron_paramdict['t_m']) * (
                        (neuron_paramdict['V_rest'] - V1) + I1 * neuron_paramdict['R'])
                V1[V1 < -neuron_paramdict['Vth'] / 10] = -neuron_paramdict['Vth'] / 10  # Limit negative potential

                # If neuron in refractory period, prevent changes to membrane potential
                refr1 = (t * sim_dict['dt'] - ts1 <= neuron_paramdict['t_refr'])
                V1[refr1] = 0

                fired = np.nonzero(V1 >= neuron_paramdict['Vth'])  # Hidden neurons that spiked
                V1[fired] = 0  # Reset their membrane potential to zero
                ts1[fired] = t  # Update their most recent spike times

                ST1 = np.zeros(network_arch_dict['n_h1'])  # Hidden layer spiking activity
                ST1[fired] = 1  # Set neurons that spiked to 1

                # Repeat the process for the output layer
                I2 = I2 + (sim_dict['dt'] / neuron_paramdict['t_syn1']) * (w_out.dot(ST1) - I2)

                V2 = V2 + (sim_dict['dt'] / neuron_paramdict['t_mH']) * (
                        (neuron_paramdict['V_rest'] - V2) + I2 * (neuron_paramdict['RH']))
                V2[V2 < -neuron_paramdict['VthO'] / 10] = -neuron_paramdict['VthO'] / 10

                refr2 = (t * sim_dict['dt'] - ts2 <= neuron_paramdict['t_refr'])
                V2[refr2] = 0
                fired2 = np.nonzero(V2 >= neuron_paramdict['VthO'])

                V2[fired2] = 0
                ts2[fired2] = t

                s2 = np.zeros((network_arch_dict['n_out']))
                s2[fired2] = 1

                test_counter = test_counter + s2

                # Compute error (used as input to error neurons)
                #Ierr = s2 - s_label[:, t]
                # Ierr = Ierr.reshape((Ierr.shape[0]))
                # Update error neurons and check for firing (positive and
                # negative error neurons)
                # If an error neuron fires, it spikes and has it membrane
                # potential decreased by VthE

                # Compute the False Positive neuron update
                #Verr1 = Verr1 + (sim_dict['dt'] * neuron_paramdict['RE'] / neuron_paramdict['t_mE']) * (Ierr)
                #Verr1[TestLabels[u]] = 0  # Setting the target label to 0 since it is not FP
                # Set the Verr from falling below the threshold and falling too negative
                #Verr1[Verr1 < -neuron_paramdict['VthE'] / 10] = -neuron_paramdict['VthE'] / 10
                # Find the fired error neurons
                #fired_err = (Verr1 >= neuron_paramdict['VthE'])
                #Verr1[fired_err] -= neuron_paramdict['VthE']
                # Note their indexes and time of fire
                #sE1 = np.zeros((network_arch_dict['n_out']))
                #sE1[fired_err] = 1
                #tsE1[fired_err] = t

                # Compute the False Negative neuron update
                #Verr2 = Verr2 + (sim_dict['dt'] * neuron_paramdict['RE'] / neuron_paramdict['t_mE']) * (-Ierr)

                # Set the Verr from falling below the threshold and falling too negative
                #Verr2[Verr2 < -neuron_paramdict['VthE'] / 10] = -neuron_paramdict['VthE'] / 10

                # Find the fired error neurons
                #fired_err = (Verr2 >= neuron_paramdict['VthE'])
                #Verr2[fired_err] -= neuron_paramdict['VthE']
                # Note their indexes and time of fire
                #sE2 = np.zeros((network_arch_dict['n_out']))
                #sE2[fired_err] = 1
                #tsE2[fired_err] = t

            tn = TestLabels[u]
            wn = np.argmax(test_counter)
            if tn == wn:
                test_predictions += 1
    print(test_predictions)

# print(f' Test Accuracy in epoch {e} is {(test_predictions / n_test)} {test_predictions}')
# test_acc[e] = 100 * (test_predictions / sim_dict['n_test'])
# return test_acc[e]

def run(config):
    return trainer_func(config)


if __name__ == '__main__':
    # import cProfile, pstats
    # pr = cProfile.Profile()
    # pr.enable()
    # from pyJoules.device import DeviceFactory
    # from pyJoules.device.rapl_device import RaplPackageDomain, RaplDramDomain
    # from pyJoules.device.nvidia_device import NvidiaGPUDomain
    # from pyJoules.energy_meter import EnergyMeter
    # from pyJoules.handler.csv_handler import CSVHandler
    # from pyJoules.handler import PrintHandler
    # domains = [RaplPackageDomain(0), NvidiaGPUDomain(0)]
    # devices = DeviceFactory.create_devices(domains)
    # meter = EnergyMeter(devices)
    # csv_handler = CSVHandler('result.csv')
    h_size = np.arange(200,300, 100)
    for i in range(len(h_size)):
        # meter.start()
        paramdict.update({'n_h1': h_size[i]})
        w_in, w_out, w_err_h1p, w_err_h1n, TrainIm, TrainLabels, TestIm, TestLabels = get_weights(paramdict)
        trainer_func(paramdict, w_in, w_out, w_err_h1p, w_err_h1n, TrainIm, TrainLabels, TestIm, TestLabels, test_flag=0)
        trainer_func(paramdict, w_in, w_out, w_err_h1p, w_err_h1n, TrainIm, TrainLabels, TestIm, TestLabels,
                     test_flag=1)
        print ("The hidden layer size is {}".format(h_size[i]))
        # csv_handler.save_data()
        # meter.stop()
        # trace = meter.get_trace()
    # ind = 0
    # paramdict.update({'n_h1': h_size[ind]})
    # print("The hidden layer size is {}".format(h_size[ind]))
    # trainer_func(paramdict, test_flag=0)

#
# @measure_energy()
# def foo():
#     pass
#
# foo()

# pr.disable()
# stats = pstats.Stats(pr).sort_stats('tottime')
# stats.dump_stats('curr_stats\profiler_stats')
# stats.print_stats()a
