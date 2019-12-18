#!/usr/bin/env python
"""Graph 201801 daily into hail clouds

"""
print(__doc__)


import numpy as np
np.random.seed(0)

from csv import writer
from os.path import basename, splitext
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import LinearSVC
from sklearn.calibration import calibration_curve
from sklearn import metrics

from sklearn.tree import export_graphviz
import pydot

from sklearn.metrics import roc_curve
from csv import reader, writer

def data(fname):
    with open(fname) as f:
        from csv import reader
        rf = reader(f)
        train = []
        y = []
        latlon = []
        for i,row in enumerate(rf):
            if i == 0:
                continue
            train_row= [float(r) for r in row[3:14]]
            ##print row
            train += [train_row,]
            y += [float(row[0]),]
            latlon += [(float(row[1]),float(row[2])),]
    return y, train, latlon

y_ice, train_ice, _ = data('ice.csv')
y_noice, train_noice, _ = data('noice.csv')
X = np.array(train_ice + train_noice)
y = np.array(y_ice + y_noice)
from os import listdir
fnames = [fn for fn in listdir('daily_cloud') if fn.endswith('.csv')]
from os.path import join, isfile
fnames = [join('daily_cloud', fn) for fn in sorted(fnames)]
for fn in fnames:
    assert isfile(fn)
if 0:
    input_fnames = [
     'entire_20171108_0000_006.csv'
    ,'entire_20171208_0000_006.csv'
    ,'entire_20180108_0000_006.csv'
    ,'entire_20180208_0000_006.csv'
    ]
elif 1:
    input_fnames = fnames
X_train = np.array(train_ice + train_noice)
y_train = np.array(y_ice + y_noice)

# Make predictions using the testing set
for fname in input_fnames:
    y_model, train_model, latlons = data(fname)    ## 5/9345
    X_test = np.array(train_model)
    y_test = np.array(y_model)

    # Create classifiers
    lr = LogisticRegression(solver='lbfgs')
    gnb = GaussianNB()
    svc = LinearSVC(C=1.0)
    rfc = RandomForestRegressor(n_estimators=6)     ## 99%, 17 errors

    # #############################################################################
    # Plot calibration plots

    plt.figure(figsize=(12, 8))
    ##ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax1 = plt.subplot2grid((3, 2), (0, 0))
    ax2 = plt.subplot2grid((3, 2), (1, 0))
    ax3 = plt.subplot2grid((3, 2), (2, 0))
    ax4 = plt.subplot2grid((3, 2), (0, 1))

    ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    rf = None
    y_pred_rf = None
    rocs = []

    if 1:
        feature_list = ['elevation',
     'high_freezing',
     'dry_mid_level1',
     'dry_mid_level2',
     'dry_mid_level3',
     'pw1',
     'pw2',
     'cape',
     'uvec',
     'vvec',
     'mag']
    for clf, name in [
            (lr, 'Logistic'),
                      (gnb, 'Naive Bayes'),
                      (svc, 'Support Vector Classification'),
                      (rfc, 'Random Forest')]:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        ##raise Exception(name, y_pred)
        fpr, tpr, _ = roc_curve(y_test, y_pred)
        rocs += [(fpr, tpr, name),]

        if name == 'Random Forest':
            y_pred_rf = y_pred
            print y_pred_rf.sum()
            errors = np.abs(y_pred_rf - y_test)
            print('rf Mean Absolute Error:', round(np.mean(errors), 2),
                    'Prob(hail).')
            # Calculate mean absolute percentage error (MAPE)
            mse = metrics.mean_squared_error(y_test, y_pred_rf)
            print 'rf mse:', mse
            print 'sum(y_test):', sum(y_test)
            print 'sum(y_pred_rf):', sum(y_pred_rf)
            assert len(latlons) == len(y_pred_rf)
            ##cloud = np.array(latlons)[y_pred_rf == 1] ## heat cloud
            if 1:
                # where predicted hail > 0
                intensity = y_pred_rf[y_pred_rf >= 0.] ## regressor
                xy = np.array(latlons)[y_pred_rf >= 0.] ## regressor
            if 1:
                # where test hail == 1
                xy_actuals = np.array(latlons)[y_test >= 1.] ## actuals
            def myfn(x):
                return x[1]
            for feature, importance in sorted(zip(feature_list,
                clf.feature_importances_), key=myfn, reverse=True):
                print (feature, importance)
            if 0:
                 if not np.allclose(sum(intensity),2330.5):
                     raise Exception(sum(intensity))
            elif 0:
                 # use world map as normalizer
                 sum_intensity = sum(intensity)
            elif 1:
                 # use a constant normalizer
                 sum_intensity = 2330.5
            london_data = []
            for i,(row,s) in enumerate(zip(xy, intensity)):
                ##if np.allclose(s,0.):
                ##    continue
                london = 51.5074,0.1278
                a,b = row
                rad = 8
                if london[0] - rad < a < london[0] + rad \
                        and london[1] - rad < b < london[1] + rad:
                    ##raise Exception(sum_intensity)
                    ##london_data += [[a,b,s],]
                    prob_hail = (s+0.)/sum_intensity * 100.
                    conditional_loss_given_hail = -0.0644
                    premium = 100*-conditional_loss_given_hail*prob_hail/(1.-prob_hail)
                    ##prob = (s+0.)/sum_intensity * 100.
                    fn, _ = splitext(basename(fname))
                    dt = fn.split('_')[1]
                    row = [dt, a, b, prob_hail, premium,]
                    ##rows += [row,]
                    with open('london_hail_2018_enlarged.csv','a') as f:
                        cf = writer(f)
                        cf.writerow(row)
