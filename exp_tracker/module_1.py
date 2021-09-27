"""
1. choose to create or open a project
2. read and write to JSON files
3. list all the .json files
"""
import json
import ipywidgets as widgets
import os


def choice_1():
    """
    return a button widget to choose
    """
    print('Create or import project?')
    button = widgets.RadioButtons(
        options=['Create new project', 'Import existing project'],
        description='Choose:',
        disabled=False
    )
    return button


def projects_lists():
    """
    return the list of the *.json  files in the ./data folder
    """
    path = "./data/"
    file_list = os.listdir(path)
    lst = []
    for item in file_list:
        if item.endswith('.json'):
            item = item.split('.')[0]
            lst.append(item)
    return lst


def choose_project_widget(lst):
    """
    return a selection widget to choose the project name
    """
    print('Please choose from the existing project: ')
    if not projects_lists():
        print('There is no project, please create one')
    else:
        choose = widgets.Dropdown(
            options=lst,
            description='Project: ',
            disabled=False
        )
        return choose


def input_name_widget():
    """
    return a text input widget
    """
    print('Please enter the name of the new project: ')
    name = widgets.Text(
            description='Project: ',
            disabled=False
    )
    return name


def project_widget(choice):
    """
    :param choice: the button widget returned by choice_1()
    :return: project name input widget or project selection widget
    """
    if choice.value == 'Create new project':
        return input_name_widget()
    else:
        return choose_project_widget(projects_lists())


def project_name_validation(choice, project):
    """
    determine if the project name is valid
    :param choice: the button widget returned by choice_1()
    :param project: project name
    :return: if the name is valid, return the project name
    """
    print('The project you choose is: {0}'.format(project.value))
    if choice.value == 'Create new project':
        if project.value in projects_lists():
            print('Project existed, please enter a new name')
            return None
        elif '.' in project.value:
            print('Project name can not include "."\nPlease enter again')
            return None
        elif project.value == '':
            print('Project name can not br empty\nPlease enter again')
            return None
        else:
            data = [{'id': 0, 'Date': '2021-01-01', 'Amount': 0,
                     'Category': 'Others', 'Description': 'Initial Value',
                     'Account': 'Cash'}]
            with open('./data/{0}.json'.format(project.value), 'w') as f:
                json.dump(data, f, indent=4)
            return project.value
    else:
        return project.value
