#!/usr/bin/env python
"""Arrange SU and non-SU into sequences

Consider two 1D sequences:

>>> X1 = [[0.5], [1.0], [-1.0], [0.42], [0.24]]
>>> X2 = [[2.4], [4.2], [0.5], [-0.24]]
To pass both sequences to fit or predict, first concatenate them into a single array and then compute an array of sequence lengths:

>>> X = np.concatenate([X1, X2])
>>> lengths = [len(X1), len(X2)]
Finally, just call the desired method with X and lengths:

>>> hmm.GaussianHMM(n_components=3).fit(X, lengths)
GaussianHMM(algorithm='viterbi', ...

"""
import numpy as np
from csv import reader
from csv import writer
from collections import defaultdict
from matplotlib.dates import YearLocator, MonthLocator
import numpy.random
from sklearn.metrics import roc_curve, auc
from scipy import interp
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)

np.random.seed(5)
def myfn():
    return 0
dt = defaultdict(myfn)
events = []
with open('mentions_eventrootcode.csv') as f:
    cf = reader(f)
    for date, event, counts in cf:
        event = int(event)
        counts = int(counts)
        events += ([date, event, counts],)
        dt[date] += counts

ratios = defaultdict(dict)
for date, event, counts in events:
    ratios[date][event] = (counts + 0.)/dt[date]

avg_gold = dict()
with open('avg.csv') as f:
    cf = reader(f)
    for date, avg, gold in cf:
        avg = float(avg)
        gold = float(gold)
        avg_gold[date] = (avg,gold)

r = []
with open('thailand_ratios.csv','w') as f:
    cf = writer(f)
    for dt in sorted(ratios):
        row = [dt,] + [ratios[dt].get(e,0) for e in range(10,15)] + \
                list(avg_gold[dt])
        cf.writerow(row)
        r += [row,]

def data(fname):
    cats = []
    dates = []
    ##with open('nonprone.txt') as f:
    with open(fname) as f:
        cf = reader(f)
        for row in cf:
            dt1, dt2 = row
            dt1 = int(dt1)
            dt2 = int(dt2)
            # one weekly sequence
            from arrow import get
            d,m = zip(*[(get(row[0],'YYYYMMDD').datetime.toordinal(),row[1:]) for row in r if dt1 < int(row[0]) <= dt2])
            assert len(d) in (6,7)
            assert len(m) in (6,7)
            assert len(d) == len(m)
            a = np.array(m)
            cats += [a,]
            dates += d
            assert a.shape[1] == 7
            from arrow import get
    dates = np.array(dates)
    X = np.concatenate(cats)
    lengths = [len(aa) for aa in cats]
    return dates, X, lengths

dates, X, lengths = data('prone.txt')
dates_np, X_np, lengths_np = data('nonprone.txt')

from hmmlearn.hmm import GaussianHMM
model = GaussianHMM(n_components=5, covariance_type="diag",
        n_iter=1000).fit(X, lengths)
model2 = GaussianHMM(n_components=5, covariance_type="diag",
        n_iter=1000).fit(X_np, lengths_np)
##raise Exception('stop')
if 1:
    from matplotlib import cm, pyplot as plt
    fig, axs = plt.subplots(model.n_components, sharex=True, sharey=True)
    hidden_states = model.predict(X)
    colours = cm.rainbow(np.linspace(0, 1, model.n_components))
    for i, (ax, colour) in enumerate(zip(axs, colours)):
        # Use fancy indexing to plot data in each state.
        mask = hidden_states == i
        ax.plot_date(dates[mask], X[mask,4], "o-", c=colour)
        ##ax.plot(X[mask,0], X[mask,1], ".-", c=colour)
        ax.set_title("hidden state {0}".format(i))

        # Format the ticks.
        ax.xaxis.set_major_locator(YearLocator())
        ax.xaxis.set_minor_locator(MonthLocator())

        ax.grid(True)
    plt.show()
if 1:
    pred = model.predict(X)
    unique, counts = numpy.unique(pred, return_counts=True)
    print (unique, counts)
    ##raise Exception
if 1:
    # have to do this manually based on SU set expects 4
    i = 0
    mean_fpr = np.linspace(0, 1, 100)
    tprs = []
    aucs = []
    ##probas_ = model.predict_proba(X)
    from sklearn.metrics import roc_curve, auc
    from scipy import interp
    if 1:
        combined =  np.r_[X, X_np]
        probas_ = model.predict_proba(combined)
        truth = np.r_[np.ones((X.shape[0],1)), np.zeros((X_np.shape[0],1))]
        assert truth.shape[0] == combined.shape[0]
        eruption_column = 4  ## get this from sorting unique,counts
    # which state is the correct one -> out of sample predict prone + some
    # portion of nonprone
    fpr, tpr, thresholds = roc_curve(truth, probas_[:, eruption_column])
    tprs.append(interp(mean_fpr, fpr, tpr))
    tprs[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs.append(roc_auc)
    plt.plot(fpr, tpr, lw=1, alpha=0.3,
             label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
    if 1:
        plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
         label='Chance', alpha=.8)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        plt.plot(mean_fpr, mean_tpr, color='b',
                 label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
                 lw=2, alpha=.8)

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                         label=r'$\pm$ 1 std. dev.')

        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic for Social Unrest - Venezuela')
        plt.legend(loc="lower right")
        plt.show()

hidden_states = model.predict(X)
np.set_printoptions(suppress=True)
print("Transition matrix")
print(model.transmat_)
print()

if 0:
    # Generate samples from trained HMM
    import matplotlib.pyplot as plt
    X, Z = model.sample(500)
    # Plot the sampled data
    # problem with this is that it is made for 2-dimensional factors, not 5
    plt.plot(X[:, 0], X[:, 4], ".-", label="observations", ms=6,
             mfc="orange", alpha=0.7)

    # Indicate the component numbers
    means = model.means_
    for i, m in enumerate(means):
        plt.text(m[0], m[1], 'Component %i' % (i + 1),
                 size=17, horizontalalignment='center',
                 bbox=dict(alpha=.7, facecolor='w'))
    plt.legend(loc='best')
    plt.show()
print("Means and vars of each hidden state")
from matplotlib import cm, pyplot as plt
fig, axs = plt.subplots(model.n_components, sharex=True, sharey=True)

# Try to map the HMM hidden states back to SU 0 -> high
mm = model.means_[:,:5]
k = mm.sum(axis=0)
closest_state = np.argmax(mm / k, axis=1).tolist()
##closest_state = np.argmax(mm / k, axis=0).tolist()
## assert fully covered
if 0: assert set(range(5)) - set(closest_state) == set() ## [3, 0, 4, 1, 0]
##raise Exception(closest_state)
##closest_state = [3,0,4,1,2]
##closest_state = [1,2,0,4]
##closest_state = [1,2,4,0]

if 1:
    k1 = mm.sum(axis=1)
    np.argmax(mm/k1,axis=1)
    ##array([1, 1, 1, 1, 1])
    np.argmax(mm/k1,axis=0)
    print np.argmax(mm, axis=0)
    ## [1 3 3 0 4]
    ##array([1, 3, 3, 0, 4])
    ##closest_state = [1,2,0,4]
    ##closest_state = [2,1,0,4]
    closest_state = [1,2,0,4]
    ##closest_state = [1,2,3,0,4]
    """
    Means and vars of each hidden state
[[ 0.79334007  0.20665993  0.          0.        ]
 [ 0.23250203  0.76749731  0.00000066  0.        ]
 [ 0.          0.07590722  0.78396347  0.1401293 ]
 [ 0.          0.          0.453958    0.546042  ]]

    """
    ##closest_state = [1,0,2,4]
    """
    Means and vars of each hidden state
[[ 0.76749731  0.00000066  0.23250203  0.        ]
 [ 0.07590722  0.78396347  0.          0.1401293 ]
 [ 0.20665993  0.          0.79334007  0.        ]
 [ 0.          0.453958    0.          0.546042  ]]

    """
    print model.transmat_[closest_state,:][:, closest_state]
##plt.title('Thailand 2015- hidden states to predict social unrest')
##plt.ylabel('social unrest ratio (EventRootCode=14)')
plt.show()

# input y prediction
dates, X
from arrow import get
from datetime import datetime
##print get(datetime.fromordinal(dates[0]))
## do this date:
## [(i,get(datetime.fromordinal(d))) for i,d in enumerate(dates) if i==49]
print model.transmat_[closest_state,:][:, closest_state]
for ix in (49, 49+7,49+7+7,49+7+7+7):
##ix = 49+7+7+7
    """
    transmat_cdf [[ 0.78396347  0.8598707   0.8598707   0.8598707   1.        ]
     [ 0.00000066  0.76749797  1.          1.          1.        ]
     [ 0.          0.20665993  1.          1.          1.        ]
     [ 0.          1.          1.          1.          1.        ]
     [ 0.453958    0.453958    0.453958    0.453958    1.        ]]
    next_state 1
    next_obs [ 0.04909566  0.11133575  0.02663514  0.03661344  0.02692243 -2.39065688
      0.21286505]

    next_state 0
    next_obs [ 0.05706419  0.0868399   0.09032652  0.05510095  0.01305004 -3.21366924
     -0.27292745]

     next_state 0
    next_obs [ 0.05706419  0.0868399   0.09032652  0.05510095  0.01305004 -3.21366924
     -0.27292745]

    """
    ix_to = np.where(np.cumsum(lengths) == ix)[0][0]
    length = lengths[ix_to]
    x = X[ix:ix+length]
    y = model.predict(x)
    dt = get(datetime.fromordinal(dates[ix]))
    dt2 = get(datetime.fromordinal(dates[ix+length]))
    ##print lengths[ix]
    last_state = y[-1]
    tm = model.transmat_[closest_state,:][:, closest_state]
    ii = np.where(closest_state == last_state)
    row = tm[ii,:]
    print '-'*60
    print tm
    print repr([dt,dt2, x, y, row])
    print '-'*60
    if 0:
        # how to predict the next state given a sequence
        # use the last element of the sequence, then find the highest element
        # of the transition probability matrix row corresponding to that state
        # then find the highest probability column

        # https://github.com/hmmlearn/hmmlearn/issues/171
        from sklearn.utils import check_random_state
        states = model.predict(x)
        transmat_cdf = np.cumsum(model.transmat_, axis=1)
        # should do multiple draws from random_state
        d = []
        for i in range(100):
            random_state = check_random_state(model.random_state)
            next_state = (transmat_cdf[states[-1]] > random_state.rand()).argmax()
            d += [next_state,]
        from scipy.stats import mode
        mean_next_state = mode(d)[0][0]
        ##next_obs = model._generate_sample_from_state(next_state, random_state)
        ##print 'next_obs', next_obs
        print 'transmat_cdf', transmat_cdf
        print 'next_state', next_state
        print 'next_state_mean', mean_next_state
        print 'y', y

"""
Current state = 2
[[ 0.76749731  0.23250203  0.00000066  0.        ]
 [ 0.20665993  0.79334007  0.          0.        ]


DATE: 2015-06-10
CURRENT STATE: 2/4 social unrest
NEXT STATE:

    SOCIAL UNREST ------------------------>
    0           1            2           3

 [ 7.59%        0.%          78.4%       14% ]

"""

raise Exception
"""
Out[31]:
array([[ 0.76749731,  0.23250203,  0.00000066,  0.        ],
       [ 0.20665993,  0.79334007,  0.        ,  0.        ],
       [ 0.07590722,  0.        ,  0.78396347,  0.1401293 ],
       [ 0.        ,  0.        ,  0.453958  ,  0.546042  ]])
"""

for i in range(model.n_components):
##for i in closest_state:
    print("{0}th hidden state".format(i))
    print("mean = ", model.means_[i])
    print("var = ", np.diag(model.covars_[i]))
    print()
    # save for later

if 0:
    colours = cm.rainbow(np.linspace(0, 1, model.n_components))
    for i, (ax, colour) in enumerate(zip(axs, colours)):
        # Use fancy indexing to plot data in each state.
        mask = hidden_states == i
        ax.plot_date(dates[mask], X[mask,4], "o-", c=colour)
        ##ax.plot(X[mask,0], X[mask,1], ".-", c=colour)
        ax.set_title("hidden state {0}".format(i))

        # Format the ticks.
        ax.xaxis.set_major_locator(YearLocator())
        ax.xaxis.set_minor_locator(MonthLocator())

        ax.grid(True)
    ##plt.title('Thailand 2015- hidden states to predict social unrest')
    ##plt.ylabel('social unrest ratio (EventRootCode=14)')
    plt.show()
    """
    In [3]: hidden_states
    Out[3]:
    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4,
           1, 1, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 2, 0,
           0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1,
           4, 4, 4, 4, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 4, 1, 1, 4,
           4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    """
