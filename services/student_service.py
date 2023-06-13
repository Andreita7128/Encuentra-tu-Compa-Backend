import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

projects_df = None
students_df = None

BALANCED = 1
BY_HARD_SKILLS = 2
BY_SOFT_SKILS = 3

def load_projects():
    global projects_df
    projects_df = pd.read_csv('./data/projects_dataset.csv')

def load_students():
    global students_df

    students_df = pd.read_csv('./data/students_dataset.csv')
    students_df = students_df.drop("Marca temporal", axis=1)

def get_team(data, _type, k):

    load_students()
    project_data = data['data']['project']
    soft_skills_data = data['data']['softSkills']
    
    global students_df
    names_column_index = 1
  
    if(_type==BY_HARD_SKILLS):
        knn_indices = get_knn_indices(project_data, students_df, k, 3, 15, 3)

    if(_type==BY_SOFT_SKILS):
        knn_indices = get_knn_indices(soft_skills_data, students_df, k, 15, 25, 0)

    if(_type==BALANCED):
        knn_indices = get_knn_balanced(project_data, soft_skills_data, students_df, 24)

    _name_list = []
    output = []
    for indx in knn_indices:
        output.append({'name':get_name_by_index(indx), 'bestHardSkill':get_best_hard_skill(indx), 'bestSoftSkill':get_best_soft_skill(indx)})

    return output
    
def get_knn_indices(project_data, students_df, k_neighbors, start_col_idx, end_col_idx, project_start):

    # Getting numeric data
    X = students_df[students_df.columns[start_col_idx:end_col_idx]].to_numpy()
    protoperson = project_data[project_start:]


    X = np.vstack((X, protoperson))
    nbrs = NearestNeighbors(n_neighbors=k_neighbors+1, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)

    return indices[len(indices)-1][1:]
   

def get_name_by_index(index):
    return students_df.loc[index, 'Nombre']

def get_best_hard_skill(index):

    row = students_df.loc[index]
    cols_names = students_df.columns[3:15]
    hardSkills = row[3:15]
    largestIndex = 0
    largestScore = float('-inf')
    for i in range(len(hardSkills)):
        if(hardSkills[i]>largestScore ):
            largestScore = hardSkills[i]
            largestIndex = i

    return cols_names[largestIndex]

def get_best_soft_skill(index):

    row = students_df.loc[index]
    cols_names = students_df.columns[15:25]
    softSkills = row[15:25]
    largestIndex = 0
    largestScore = float('-inf')
    for i in range(len(softSkills)):
        if(softSkills[i]>largestScore ):
            largestScore = softSkills[i]
            largestIndex = i

    return cols_names[largestIndex]


def find_k_rows(matrix, k):
    row_sums = [(sum(row), i) for i, row in enumerate(matrix)]
    row_sums.sort(reverse=True)  # Sort the row sums in descending order
    
    return [row_idx for _, row_idx in row_sums[:k]]
    
def get_knn_balanced(project_data, soft_skills_data, students_df, k_neighbors):

    X = students_df[students_df.columns[3:15]].to_numpy()
    protoperson = project_data[3:]

    X = np.vstack((X, protoperson))
    nbrs = NearestNeighbors(n_neighbors=k_neighbors+1, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)


    Y = students_df[students_df.columns[15:25]].to_numpy()
    protopersonY = soft_skills_data

    Y = np.vstack((Y, protopersonY))
    nbrs = NearestNeighbors(n_neighbors=k_neighbors+1, algorithm='ball_tree').fit(Y)
    distancesY, indicesY = nbrs.kneighbors(Y)

    reversed_indicesY = indicesY[:, ::-1]

    reversed_indicesY_last = reversed_indicesY[-1][:-1]
    indices_last = indices[-1][1:]

 
    balanced = []

    for i in range(24):
        balanced.append({'score': 0, 'index': i})

    for i in range(24):
        score = i
        index = reversed_indicesY_last[i]
        balanced[index]['score'] += score

    for i in range(24):
        score = i
        index = indices_last[i]
        balanced[index]['score'] += score

    
    sorted_balanced = sorted(balanced, key=lambda x: x['score'], reverse=False)
 
    output = []
    for i in range(len(sorted_balanced)):
        if(len(output)<=5 and i%round((len(sorted_balanced)/5), 0))==0:
            print(i)
            output.append(sorted_balanced[i]['index'])
    
    return output