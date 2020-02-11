#!/usr/bin/env python
"""
author: Michael Yang

Note: "team vs. team data doesn't mean shit" -Mello

Mello 1.7
REM. SALARY:
$500
Pos Player  FPPG
QB  Tony Romo   20.7
RB  James Starks    12.2
RB  Le'Veon Bell    15.0
WR  Josh Gordon 19.9
WR  Vincent Jackson 19.5
TE  Greg Olsen  11.1
FLEX    Pierre Garcon P 16.3
K   Blair Walsh P   7.7
DST Rams    8.9

Serrano 1.5
REM. SALARY:
$100
Pos Player  FPPG
QB  Aaron Rodgers   23.3
RB  Bilal Powell    10.3
RB  Marshawn Lynch P    17.2
WR  Stevie Johnson P    13.5
WR  Brandon Marshall    19.7
TE  Jordan Reed 14.6
FLEX    Steve Smith 11.9
K   Garrett Hartley 9.9
DST Chiefs  16.1

George 1.3
REM. SALARY:
$400
Pos Player  FPPG
QB  Michael Vick O  18.2
RB  James Starks    12.2
RB  Jamaal Charles P    24.0
WR  Eddie Royal Q   12.3
WR  Josh Gordon 19.9
TE  Jimmy Graham Q  23.3
FLEX    Jordan Cameron  18.5
K   Mason Crosby    11.9
DST Chiefs  16.1

Justice 1.5
REM. SALARY:
$200
Pos Player  FPPG
QB  Tony Romo   20.7
RB  Danny Woodhead  15.8
RB  Fred Jackson P  16.0
WR  Dez Bryant  20.7
WR  Julian Edelman P    13.8
TE  Jordan Cameron  18.5
FLEX    Eddie Royal Q   12.3
K   Dan Bailey  9.8
DST Chiefs  16.1

George's team was the nearest to the default Avg. Points Score.
Steve's team requires the most biasing to achieve his team.

Metateam 1.9
REM. SALARY:
$100
Pos Player  FPPG
QB  Aaron Rodgers   23.3
RB  Fred Jackson P  16.0
RB  Bilal Powell    10.3
WR  Vincent Jackson 19.5
WR  Pierre Garcon P 16.3
TE  Jordan Reed 14.6
FLEX    Josh Gordon 19.9
K   Mason Crosby    11.9
DST Chiefs  16.1

Betting Strategy 11/3/2013 1:00p

each team (4) in:
Entry Fee = $50 Prize Pool = $225
1st: $150, 2nd: $75

Justice also in Entry Fee = $20 Prize Pool = $90  (error)
1st: $60, 2nd: $30

each team (4) in:
Entry Fee = $11 Prize Pool = $50K "Hail Mary"
1st $4,000 + Fantasy Millionaire Grand Final Entry ($1,500)
2nd $2,500 + Fantasy Millionaire Grand Final Entry ($1,500)
3rd $1,750 + Fantasy Millionaire Grand Final Entry ($1,500)
4th $1,250 + Fantasy Millionaire Grand Final Entry ($1,500)
5th $1,000
6th $750
7th $525

metateam in Entry Fee = $11 Prize Pool = $50K
metateam in $1,060 Head-to-Head vs. CONDIA (Prize Pool $2,000)

Lineup in order:

Justice @ 1.5
Mello @ 1.7
Meta @ 1.9
Serrano @ 1.5
George @ 1.3
==
Model alteration:

Inconsistency = risk

QB: highest producing score, not consistent
RB: most consistent
WR: highly inconsistent
TE: high inconsistent
K: whatever, pick on high-scoring, teams who can't finish

highest -> lowest inconsistent (risk):
WR, TE, QB, RB

Risk dependent on weather, dome/not dome, QB running the ball.
QB who runs the ball the most if he can't throw
e.g. Cam Newton

fantasy model alteration:
if cold/snowing/raining and not dome:
    downweight QB by 10%, WR by 10%,
    upweight RB by 20%
    and if QB good runner, upweight QB by 10%

see: weatherunderground.com

Justice @ 1.5
Mello @ 1.7
Meta @ 1.9
Serrano @ 1.5
George @ 1.3
==
2013111
jobs:0 $ ./t 2.1
Team: Justice 10-team league 8-0 20131110
=================================================================
Position        Name           Salary  AvgPts       GameInfo
=================================================================
QB        Tony Romo         +    9700  21.124  Dal@NO 08:30PM ET
RB        Frank Gore        +    6700  15.675  Car@SF 04:05PM ET
RB        Danny Woodhead    +    5600  16.175  Den@SD 04:25PM ET
WR        Mike Wallace      +    5400  12.250  Mia@TB 08:40PM ET
WR        Eddie Royal q          3000  12.688  Den@SD 04:25PM ET
TE        Jason Witten      +    6000  13.944  Dal@NO 08:30PM ET
RB (f)    Fred Jackson      +    5700  15.411  Buf@Pit 01:00PM ET
K         Matt Prater            3900  11.375  Den@SD 04:25PM ET
DST       Titans            +    4000  10.250  Jax@Ten 01:00PM ET
=================================================================
Total Salary: 50000
-----------------------------------------------------------------
     Name      Not Selected
===========================
Pierre Garcon  -
Dan Bailey     -
--------------------
multiplier: 2.10


"""

from utils.vis import displayTable

def print_row(x, isflex=False, selected=False):
    selected_print = ' '
    if selected:
        selected_print = '+'
    if not isflex:
        name = ' '.join([x['Name'], x['Status']])
        if x['Position'] == 'DST':
            name = name + ' ' * (16-len(name))
        row = (x['Position'],name,selected_print,x['Salary'],
            x['AvgPointsPerGame'],x['GameInfo'])
    elif isflex:
        row = (x['Position'] + " (f)",x['Name'], selected_print, x['Salary'],x['AvgPointsPerGame'],x['GameInfo'])
    return row

from csv import reader
## Parse in salaries/avg. points per game
with open('DKSalaries.csv') as f:
    cf = reader(f)
    rows = []
    for i,row in enumerate(cf):
        if i == 0:
            assert row == ['Position', 'Name', 'Salary', 'GameInfo', 'AvgPointsPerGame']
            header = row
            continue
        if row[0][0] == '#':
            continue
        rowdict = dict(zip(header,row))
        rowdict = dict([(k,v.strip()) for k,v in rowdict.items()])
        rows += [rowdict,]

# 20131102 08:03 AM
out = [
   'Michael Vick',
   ##'Victor Cruz',  ## out as of 20131228, reinstated 20140802
   'Edwin Baker',
     ]

probable = [
##    'Blair Walsh',
##    'Pierre Garcon',
##    'Fred Jackson',
##    'Julian Edelman',
##    'Jamaal Charles',
##    'Marshawn Lynch',
##    'Stevie Johnson',
    ##'Marvin Jones',  ## tweaked ankle 20131228, persisting July 21, 2014
    ]

injured = [
        'Rob Gronkowski',  ## last info 2013122013
        'Owen Daniels',  ## Injured reserve 20140802
        'Jordan Cameron',
        'Jordan Reed',
        'Jason Witten',  ## 20140910 - not doing too well
        ]

daytoday = [
    ##'Nate Burleson',
    ##'Terrelle Pryor',
    #'Denarius Moore',
    'Marvin Jones',  ## tweaked ankle 20131228, persisting July 21, 2014
    ]

questionable = [
    ('None',1.0),
    ##('Eddie Royal', 0.9),  # expect him to get on the field and play
##    ('Jimmy Graham',1.0),  # one bad foot last week caught two touchdown passes, likely he'll play
    ##('Jordan Cameron',0.9), # 7/29/2014 he's good
    ]

QBInflate = 1.4
RBInflate = 1.3
ProbableDeflate = 1.0   # Probable = 100%, check later
##DayToDayDeflate = 1.0   # Day to Day
DayToDayDeflate = 0.5   # Day to Day

newrows = []
for row in rows:
    row['Status'] = ''
    if row['Name'] in out:
        row['AvgPointsPerGame'] = '0'
        row['Status'] = 'o'
    if row['Name'] in injured:
        row['AvgPointsPerGame'] = '0'
        row['Status'] = 'ir'
    if row['Name'] in probable:
        row['AvgPointsPerGame'] = str(float(row['AvgPointsPerGame']) * ProbableDeflate)
        row['Status'] += 'p'
    if row['Name'] in daytoday:
        row['AvgPointsPerGame'] = str(float(row['AvgPointsPerGame']) * DayToDayDeflate)
        row['Status'] += 'dtd'
    if row['Name'] in zip(*questionable)[0]:
        i = zip(*questionable)[0].index(row['Name'])
        reduction = questionable[i][1]
        row['AvgPointsPerGame'] = str(float(row['AvgPointsPerGame']) * reduction)  # Varies by player
        row['Status'] += 'q'
    if row['Position'] == 'QB':
        row['AvgPointsPerGame'] = str(float(row['AvgPointsPerGame']) * QBInflate)
    if row['Position'] == 'RB':
        row['AvgPointsPerGame'] = str(float(row['AvgPointsPerGame']) * RBInflate)
    newrows += [row,]
rows = newrows

# augment avg. points by ESPN fantasy team
if 0:
    teamName = 'unbiased - use avg. points per game as score'
    selections = []
elif 1:
    teamName = "Winner of 20140907"
    teamName += 'head to head against YKYA111'
    selections = [
            'Peyton Manning'
            ,'Knowshon Moreno'
            ,'Jamaal Charles'
            ,'Anquan Boldin'
            ,'Brandin Cooks'
            ,'Julio Jones'
            ,'Ladarius Green'
            ,'Rashad Jennings'
            ,'Panthers'
            ]
elif 0:
    # 1.5
    teamName = "Justice's picks - 10 team league"
    teamName += ' 6-1 20131101'
    selections = [
       'Tony Romo',
       'Frank Gore',
       'Fred Jackson',
       'Steven Jackson',
       'Danny Woodhead',
       'Dez Bryant',
       'Matt Prater',
       'Dan Bailey',
       'Chiefs',
        ]
elif 0:
    # 1.7
    teamName = 'Mello 14-team league'
    teamName += ' 7-0 20131101'
    selections = [
     'Tony Romo'
    ,'Marshawn Lynch'
    ,'Vincent Jackson'
    ,'Josh Gordon'
    ,"Le'Veon Bell"
    ,'Denarius Moore'
    ,'Pierre Garcon'
    ,'Greg Olsen'
    ,'Blair Walsh'
    ,'Rams'
    ]
elif 0:
    # 1.9
    teamName = "Mello Plummer Serrano Justice Superpick"
    selections = [
    'Tony Romo'
   ,'Marshawn Lynch'
   ,'Vincent Jackson'
   ,'Josh Gordon'
   ,"Le'Veon Bell"
   ,'Denarius Moore'
   ,'Pierre Garcon'
   ,'Greg Olsen'
   ,'Blair Walsh'
   ,'Rams',
    'Aaron Rodgers',
    'Brandon Marshall',
    'Steve Smith',
    'Marshawn Lynch',
    'Bilal Powell',
    'Jordan Reed',
    'Stevie Johnson',
    'Buccaneers',
   'Jamaal Charles',
   'Jimmy Graham',
   'Andy Dalton',
   'Vincent Jackson',
   'Josh Gordon',
   'Torrey Smith',
   'Mason Crosby',
   'Chiefs',
    'Tony Romo',
    'Frank Gore',
    'Fred Jackson',
    'Steven Jackson',
    'Danny Woodhead',
    'Dez Bryant',
    'Matt Prater',
    'Dan Bailey',
    'Chiefs',
        ]
elif 0:
    # 2.2
    teamName = 'Serrano 12-team league'
    teamName += ' 6-1 20131101'
    selections = [
        'Aaron Rodgers',
        'Brandon Marshall',
        'Steve Smith',
        'Marshawn Lynch',
        'Bilal Powell',
        'Jordan Reed',
        'Stevie Johnson',
        'Buccaneers',
        ]
elif 0:
    # 1.3 - Jake Locker
    # 1.4 - Mike Glennon - George's pick
    # 1.8 - most of the picks
    # ESPN Fantasy recommends Jake Locker
    teamName = 'George Plummer 4-team league'
    teamName += ' 7-0 20131101'
    selections = [
        'Jamaal Charles',
        'Jimmy Graham',
        'Andy Dalton',
        'Vincent Jackson',
        'Josh Gordon',
        'Torrey Smith',
        'Mason Crosby',
        'Chiefs',
        ]
elif 0:
    #
    teamName = 'Justice 10-team league'
    teamName += ' 8-0 20131110'
    selections = [
            'Tony Romo',
            'Frank Gore',
            'Fred Jackson',
            'Mike Wallace',
            'Pierre Garcon',
            'Jason Witten',
            'Danny Woodhead',
            'Titans',
            'Dan Bailey',
            ]

if selections != []:
    print 'Using bias: %s' % '\n'.join(selections)

if 1:
    import sys
    if not len(sys.argv) == 2:
        print "Usage: %s %s" % (sys.argv[0], 'multiplier (1.0 - 3.0)')
    multiplier = float(sys.argv[1])
    ##multiplier = 1.2  ## not biased enough
    ##multiplier = 1.3  ## everybody except QB, DST, K, Flex
    ##multiplier = 1.4  ## everybody except RB, TE, DST
    ##multiplier = 1.5  ## Cowboys D, everybody except RB, TE, DST
    ##multiplier = 1.7  ## Cowboys D, everybody except RB, DST
    ##multiplier = 1.8  ## Vikings D, Replace Le'Veon Bell with Marshawn Lynch
    ##multiplier = 1.9
    ##multiplier = 2
    ##multiplier = 2.161995   ## no slack in Salary constraint (Vikings/Lynch)
    ##multiplier = 2.161997 ## slack in Salary constraint (Rams/Le'Veon)
    ##multiplier = 2.2
    ##multiplier = 2.5
    ##multiplier = 2.8
    ##multiplier = 3  ## Rams D, Pierre Garcon, Le'Veon Bell

newrows = []
for row in rows:
    row['Score'] = row['AvgPointsPerGame']
    if row['Name'] in selections:
        row['Score'] = str(float(row['Score']) * multiplier)
    newrows += [row,]
rows = newrows
del newrows

##KICKER = True
KICKER = False  ## 3 WR

if KICKER:
    assert sorted(set([row['Position'] for row in rows])) == ['DST', 'K', 'QB', 'RB', 'TE', 'WR']
else:
    assert sorted(set([row['Position'] for row in rows])) == ['DST', 'QB', 'RB', 'TE', 'WR']
QBs = [row for row in rows if row['Position'] == 'QB']
RBs = [row for row in rows if row['Position'] == 'RB']
WRs= [row for row in rows if row['Position'] == 'WR']
TEs= [row for row in rows if row['Position'] == 'TE']
FLEXs = RBs + WRs + TEs
Ks = [row for row in rows if row['Position'] == 'K']
DSTs = [row for row in rows if row['Position'] == 'DST']
# QB RB WR TE FLEX K DST
##   FLEX is any of a {RB, WR, TE}
## 9 total positions
if 1:
    if KICKER:
        nPlayers = [1,2,2,1,1,1,1]
    elif not KICKER:
        nPlayers = [1,2,3,1,1,0,1]
elif 0:
    nPlayers = [2,2,3,1,1,0,0]

# min: -AvgPointsPerGame*posN
mineq = ' '.join(['-'+str(row['Score']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(QBs)])
mineq += ' '.join(['-'+str(row['Score']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(RBs)])
mineq += ' '.join(['-'+str(row['Score']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(WRs)])
mineq += ' '.join(['-'+str(row['Score']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(TEs)])
mineq += ' '.join(['-'+str(row['Score']) + ' ' +
     'flex' + str(i)
        for i,row in enumerate(FLEXs)])
mineq += ' '.join(['-'+str(row['Score']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(Ks)])
mineq += ' '.join(['-'+str(row['Score']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(DSTs)])

# sal: cost*posN <= 50000
saleq = ' '.join([str('+'+row['Salary']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(QBs)])
saleq += ' '.join(['+'+str(row['Salary']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(RBs)])
saleq += ' '.join(['+'+str(row['Salary']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(WRs)])
saleq += ' '.join(['+'+str(row['Salary']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(TEs)])
saleq += ' '.join(['+'+str(row['Salary']) + ' ' +
     'flex' + str(i)
        for i,row in enumerate(FLEXs)])
saleq += ' '.join(['+'+str(row['Salary']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(Ks)])
saleq += ' '.join(['+'+str(row['Salary']) + ' ' +
    row['Position'].lower() + str(i)
        for i,row in enumerate(DSTs)])

saleq += ' <= 50000'
# qb: +qb1 + qb2 + ... = 1
qbeq = ' '.join(['+' + row['Position'].lower() + str(i)
        for i,row in enumerate(QBs)])
qbeq += " = " + str(nPlayers[0])
# rb: +rb1 + rb2 + ... = 2
rbeq = ' '.join(['+' + row['Position'].lower() + str(i)
        for i,row in enumerate(RBs)])
rbeq += " = " + str(nPlayers[1])
# wr: +wr1 + wr2 + ... = 2
wreq = ' '.join(['+' + row['Position'].lower() + str(i)
        for i,row in enumerate(WRs)])
wreq += " = " + str(nPlayers[2])
# te: +te1 + te2 + ... = 1
teeq = ' '.join(['+' + row['Position'].lower() + str(i)
        for i,row in enumerate(TEs)])
teeq += " = " + str(nPlayers[3])
# fl: +fl1 + fl2 + ... = 1
flexeq = ' '.join(['+' + 'flex' + str(i)
        for i,row in enumerate(FLEXs)])
flexeq += " = " + str(nPlayers[4])
# k: +k1 +K2 + ... = 1
keq = ' '.join(['+' + row['Position'].lower() + str(i)
        for i,row in enumerate(Ks)])
keq += " = " + str(nPlayers[5])
# dst: +dst1 +dst2 +... = 1
dsteq = ' '.join(['+' + row['Position'].lower() + str(i)
        for i,row in enumerate(DSTs)])
dsteq += " = " + str(nPlayers[6])

# flex different from RB, WR, TE
# flex is any of a {RB, WR, TE}

iflex = 0
rbflexeq = ''
for i,row in enumerate(RBs):
    rbflexeq += 'rbflex%d:' % i + '+' + row['Position'].lower() + str(i) + ' +flex' +str(iflex) + ' <= 1;'
    iflex += 1
    rbflexeq += '\n'
wrflexeq = ''
for i,row in enumerate(WRs):
    wrflexeq += 'wrflex%d:' % i + '+' + row['Position'].lower() + str(i) + ' +flex' +str(iflex) + ' <= 1;'
    iflex += 1
    wrflexeq += '\n'
teflexeq = ''
for i,row in enumerate(TEs):
    teflexeq += 'teflex%d:' % i + '+' + row['Position'].lower() + str(i) + ' +flex' +str(iflex) + ' <= 1;'
    iflex += 1
    teflexeq += '\n'

#binary equation: bin [positions]

bineq = ' '.join([row['Position'].lower() + str(i)
        for i,row in enumerate(QBs)])
bineq += ' ' + ' '.join([row['Position'].lower() + str(i)
        for i,row in enumerate(RBs)])
bineq += ' ' + ' '.join([row['Position'].lower() + str(i)
        for i,row in enumerate(WRs)])
bineq += ' ' + ' '.join([row['Position'].lower() + str(i)
        for i,row in enumerate(TEs)])
bineq += ' ' + ' '.join(['flex' + str(i)
        for i,row in enumerate(FLEXs)])
bineq += ' ' + ' '.join([row['Position'].lower() + str(i)
        for i,row in enumerate(Ks)])
bineq += ' ' + ' '.join([row['Position'].lower() + str(i)
        for i,row in enumerate(DSTs)])

if KICKER:
    eqnOut = """
min: %s;
sal: %s;
qb: %s;
rb: %s;
wr: %s;
te: %s;
flex: %s;
k: %s;
dst: %s;
%s
%s
%s
bin %s;
"""
    eqnOut %= (mineq, saleq, qbeq, rbeq, wreq, teeq, flexeq, keq, dsteq,
        rbflexeq,wrflexeq,teflexeq,
        bineq)
else:
    eqnOut = """
min: %s;
sal: %s;
qb: %s;
rb: %s;
wr: %s;
te: %s;
flex: %s;
dst: %s;
%s
%s
%s
bin %s;
"""
    eqnOut %= (mineq, saleq, qbeq, rbeq, wreq, teeq, flexeq, dsteq,
        rbflexeq,wrflexeq,teflexeq,
        bineq)

with open('test.lp','wb') as fout:
    fout.write(eqnOut)
if 1:
    from utils.tools import runp
    out = runp('lp_solve -lp test.lp', verbose=False)
    # no kicker leads to bad test.lp file (k: constraint has no variables)
    """
flex: +flex0 +flex1 +flex2 +flex3 +flex4 +flex5 +flex6 +flex7 +flex8 +fl
k:  = 0;
dst: +dst0 +dst1 +dst2 +dst3 +dst4 +dst5 +dst6 +dst7 +dst8 +dst9 +dst10
"""

    found = False
    salaryCheck = 0
    print 'Team: ' + teamName
    print '='*65
    rows_print = []
    selection_rows = []
    iSelections = []
    noselection_rows = []
    for row in out.strip().split('\n'):
        if row.strip() == 'Actual values of the variables:':
            found = True
            continue
        if not found:
            continue
        variable, used = row.split()
        if int(used) == 1:
            ##print variable + '\t',
            isflex = False
            selected = False
            if variable[0] == 'q':
                n = int(variable[2:])
                row = QBs[n]
            elif variable[0] == 'r':
                n = int(variable[2:])
                row = RBs[n]
            elif variable[0] == 'w':
                n = int(variable[2:])
                row = WRs[n]
            elif variable[0] == 't':
                n = int(variable[2:])
                row = TEs[n]
            elif variable[0] == 'f':
                n = int(variable[4:])
                row = FLEXs[n]
                isflex = True
            elif variable[0] == 'k':
                n = int(variable[1:])
                row = Ks[n]
            elif variable[0] == 'd':
                n = int(variable[3:])
                row = DSTs[n]
            if row['Name'] in selections:
                selected = True
                if 0:
                    selections[selections.index(row['Name'])] += '-|'
                elif 1:
                    iSelected = selections.index(row['Name'])
                    selection_rows += [(selections[iSelected], '+'),]
                    iSelections += [iSelected,]
            row_print = print_row(row, isflex=isflex, selected=selected)
            rows_print += [row_print,]
            salaryCheck += int(row['Salary'])
    if 0: headings = ('Position','Name','Salary','AvgPts','GameInfo')
    if 1: headings = ('Position','Name','','Salary','AvgPts','GameInfo')
    print displayTable(rows=rows_print, headings=headings)
    print '='*65
    print 'Total Salary: %d' % salaryCheck
    print '-'*65
    if 0:
        print displayTable(rows=selection_rows, headings=('Name','Selected'))
        print '-'*30
    noselection_rows = [(selections[ii],'-') for ii in [i for i in range(len(selections)) if i not in
        iSelections]]
    if selections == []:
        pass
    else:
        print displayTable(rows=noselection_rows, headings=('Name','Not Selected'))
        print '-'*20
    print 'multiplier: %s' % multiplier
