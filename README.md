## Does an increased risk of climate shocks affect individual resource extraction behaviour?

This research project aims to investigate the impact of heightened risk from
climate-related shocks on individual behaviors regarding resource extraction. In an era
where climate change is increasingly affecting various aspects of life, understanding
how these risks alter human behavior, particularly in the context of resource
utilization, is crucial.

The study focuses on analyzing individual decision-making processes in scenarios with
varying degrees of climate risk. Using a combination of empirical data analysis and
behavioral modeling, we seek to identify patterns and shifts in resource extraction
practices. This includes examining factors such as resource scarcity, perception of
climate risk, economic pressures, and adaptive strategies.

## Contents

In this project, I used my Research Module in Applied Microeconomics where I built the
instrument for experimental study using O-tree, which I have used in BonnEconLab to run
the experiment and obtain the raw data set. I then use this data set to perform data
cleaning and data analysis. I wrote 6 scripts to clean the data and transform it to the
format required for analysis. These produced clean data is then used to produce plots of
subjects behaviour and subject summary statistics. On top this raw data set, I have
produced an excel file containing data for Nash equilibrium visualization for my Game
Theoretical Prediction. The main output of this project is a pdf latex file containing
game design, game theoretical prediction of the experiment and a simple graph and
summary data statistics of the lab randomization results of my otree codes.

## Size of the project:

| Language   | Files   | Blank   | Comment   | Code   |
| ---------- | ------- | ------- | --------- | ------ |
| XML        | 4       | 0       | 42        | 4962   |
| Python     | 39      | 724     | 277       | 3355   |
| HTML       | 45      | 605     | 0         | 2861   |
| TeX        | 27      | 268     | 48        | 1070   |
| YAML       | 4       | 0       | 4         | 148    |
| Text       | 4       | 0       | 0         | 143    |
| CSV        | 2       | 0       | 0         | 78     |
| Markdown   | 2       | 26      | 0         | 62     |
| TOML       | 1       | 11      | 0         | 38     |
| JSON       | 1       | 0       | 0         | 1      |
| ---------- | ------- | ------- | --------- | ------ |
| SUM:       | 129     | 1634    | 371       | 12718  |

## Tests

I tested all data cleaning process particularly to transform the data from wide to long

## Libraries used:

In addition to the libraries made available from the project template, I used

- matplotlib
- seaborn
- stargazer

[![image](https://img.shields.io/github/actions/workflow/status/Patty-pat/ClimateRiskResourceBehavior/main.yml?branch=main)](https://github.com/Patty-pat/ClimateRiskResourceBehavior/actions?query=branch%3Amain)
[![image](https://codecov.io/gh/Patty-pat/ClimateRiskResourceBehavior/branch/main/graph/badge.svg)](https://codecov.io/gh/Patty-pat/ClimateRiskResourceBehavior)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Patty-pat/ClimateRiskResourceBehavior/main.svg)](https://results.pre-commit.ci/latest/github/Patty-pat/ClimateRiskResourceBehavior/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage

To get started, create and activate the environment with

```console
$ conda/mamba env create
$ conda activate cprs
```

To build the project, type

```console
$ pytask
```

To run O-TREE game on developer server, type

```console
$ pip install -U otree
$ otree devserver
```

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).

The latex template of this paper was created by GaudeckerEconProjectTemplates.

O-tree software was developed by - Chen, D.L., Schonger, M., Wickens, C., 2016. oTree -
An open-source platform for laboratory, online and field experiments. Journal of
Behavioral and Experimental Finance, vol 9: 88-97
