import pandas as pd
import numpy as np
from scipy.stats import kendalltau
import os
from os import listdir
from os.path import isfile, join
import re
import nltk

# Get Kendal Tau value of two lists


def computeKendalT(l1, l2):
    l1 = l1[:min(len(l1), len(l2))]
    l2 = l2[:min(len(l1), len(l2))]
    tau, p_val = kendalltau(l1, l2)
    return tau


def computeJaccardDistance(l1, l2):
    return nltk.jaccard_distance(set(l1), set(l2))

# Create a new DataFrame contraining the Kendal Tau values based on the common column names of the DataFrames
# Each cell in the DataFrames contains a stringified List


def parseDataframes(df, df2, top_k):
    common_cols = list(set(df.columns[1:]).intersection(df2.columns))
    new_cols = []
    for col in common_cols:
        new_cols.append(col + ' KendalT')
        new_cols.append(col + ' Jaccard')
    result_df = pd.DataFrame(columns=new_cols)
    for row in range(df.shape[0]):
        new_row = []
        for col in common_cols:
            kendalT = computeKendalT(eval(df[col][row])[:top_k if top_k != 0 else len(
                df)], eval(df2[col][row])[:top_k if top_k != 0 else len(df2)])
            new_row.append(round(kendalT, 2))
            jaccard = computeJaccardDistance(eval(df[col][row])[:top_k if top_k != 0 else len(
                df)], eval(df2[col][row])[:top_k if top_k != 0 else len(df2)])
            new_row.append(round(jaccard, 2))
        result_df.loc[row] = new_row
    result_df['Topics'] = df[df.columns[0]]
    result_df = result_df.set_index('Topics')
    return result_df

# Read CSVs (part A, part B) and export the combined result to a new CSV


def mergeParts(countries):
    for country in countries:
        for player in range(1, 3):
            df1 = pd.read_csv('PartialResults/'+country +
                              '_'+str(player)+'_a.csv')
            df2 = pd.read_csv('PartialResults/'+country +
                              '_'+str(player)+'_b.csv')
            df = pd.concat([df1, df2], axis=0).reset_index(drop=True)
            if not os.path.exists('MergedResults'):
                os.mkdir('MergedResults')
            df.to_csv('MergedResults/'+country+'_'+str(player) +
                      '.csv', index=False, encoding='utf-8')


def allowMergingInput():
    response = -1
    while response != 0 and response != 1:
        if response != -1:
            print('Wrong Input.\nExpecting  \"0\" or \"1\"  as input.')
        try:
            response = int(
                input('Merge Part A with Part B for each csv?\n\"0\": No\n\"1\": Yes\n'))
        except ValueError:
            print('Not an Integer.')
    return response


def getCountries():
    # { Country : (player, part) }
    country_dict = {}
    for f in listdir(os.path.join(os.getcwd(), 'PartialResults')):
        filename = re.match(r'^([A-z]+)_([12])(?:_([ab]))?\.csv', f)
        if filename != None:
            if filename.group(1) not in country_dict.keys():
                country_dict[filename.group(1)] = []
            if filename.group(3) != None:
                country_dict[filename.group(1)].append(
                    (filename.group(2), filename.group(3)))
            else:
                country_dict[filename.group(1)].append(filename.group(2))
    return list(country_dict.keys())


if __name__ == '__main__':
    countries = getCountries()
    if allowMergingInput() == 1:
        try:
            mergeParts(countries)
        except:
            print('Merge_CSV process failed.')
    results = {}
    for country in countries:
        for i in range(1, 3):
            results[country + '_' +
                    str(i)] = pd.read_csv('MergedResults/' + country + '_' + str(i) + '.csv')                    
    if not os.path.exists('Results'):
        os.mkdir('Results')
    for top_k in [5, 10, 15, 0]:
        # For each country, evaluate pair of players
        for country in countries:
            if not os.path.exists('Results/' + ('Top_' + str(top_k) if top_k != 0 else 'All') + '_PlayersAsPairs'):
                os.mkdir('Results/' + ('Top_' + str(top_k) if top_k != 0 else 'All') + '_PlayersAsPairs')
            parseDataframes(results.get(country + '_1'), results.get(country + '_2'), top_k) \
                .to_csv('Results/' + ('Top_' + str(top_k) if top_k != 0 else 'All') + '_PlayersAsPairs/'
                        + country +
                        ('_Top' + str(top_k) if top_k != 0 else '_All')
                        + '_Results.csv', encoding='utf-8')
        # For each pair of countries, evaluate corresponding players
        countries.append(countries[0])
        for i in range(1, 3):
            for country1, country2 in zip(countries, countries[1:]):
                if not os.path.exists('Results/' + ('Top_' + str(top_k) if top_k != 0 else 'All') + '_CountriesAsPairs'):
                    os.mkdir('Results/' + ('Top_' + str(top_k) if top_k != 0 else 'All') + '_CountriesAsPairs')
                parseDataframes(results.get(country1 + '_' + str(i)), results.get(country2 + '_' + str(i)), top_k) \
                    .to_csv('Results/' + ('Top_' + str(top_k) if top_k != 0 else 'All') + '_CountriesAsPairs/'
                            + country1 + '_' + country2 + '_' + str(i) +
                            ('_Top' + str(top_k) if top_k != 0 else '_All')
                            + '_Results.csv', encoding='utf-8')
        countries = countries[:-1]
