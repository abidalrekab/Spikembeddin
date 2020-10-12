from brian2 import *
import matplotlib.pylab as plt
from load_embeddings import load_embeddings
data, n_nodes, embeddings_dim = load_embeddings()
def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')

taum = 2*ms
taue = 5*ms
taui = 10*ms
Vt1 = -50*mV
Vr1 = -65*mV
Vt2 = -55*mV
Vr2 = -60*mV
El = -49*mV

eqs = '''
dv/dt  = (ge+gi-(v-El))/taum : volt (unless refractory)
dge/dt = -ge/taue : volt
dgi/dt = -gi/taui : volt
'''
refractor1 = '5*ms'
refractor2 = '10*ms'

#refractor = 'v >= 0*mV'
#refractor='(1 + 2*rand())*ms'
Pop_n = 300

P = NeuronGroup(Pop_n, eqs, threshold='v>Vt1', reset='v = Vr1', refractory=refractor1,
                method='exact')
Q = NeuronGroup(Pop_n, eqs, threshold='v>Vt2', reset='v = Vr2', refractory=refractor2,
                    method='exact')

# P.v = 'Vr + rand() * (Vt - Vr)'
P.v = 100* data[0,:]*mV
Q.v = -45*mV
P.ge = 0*mV
P.gi = 0*mV

we = (8.2*0.27/100)*mV # excitatory synaptic weight (voltage)
wi = (-12*4.5/100)*mV # inhibitory synaptic weight

Ce1 = Synapses(P, P, on_pre='ge += we')
Ci1 = Synapses(P, P, on_pre='gi += wi')
Ce1.connect(condition = 'abs(j-i) == 1 and  i<225')
#Ci1.connect(condition = 'abs(j - i) <= 5 and i>=225', )
Ci1.connect(condition = ' j!=i and i>=225', p = 0.95)
wk = (8.2*0.27/100)*mV # excitatory synaptic weight (voltage)
wq = (-1*4.5/100)*mV # inhibitory synaptic weight
Ce2 = Synapses(Q,P, on_pre='gi += wq')
Ce2.connect(condition='j==i')
s_mon1 = SpikeMonitor(P)
s_mon2 = SpikeMonitor(Q)
run(1 * second)

plot(s_mon1.t/ms, s_mon1.i, ',k')
xlabel('Time (ms)')
ylabel('Neuron index g1')
show()
#visualise_connectivity(Ci)
plot(s_mon2.t/ms, s_mon2.i, ',k')
xlabel('Time (ms)')
ylabel('Neuron index g2')
show()