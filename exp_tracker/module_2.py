"""
1. display_transaction(): display all the transactions
2. add_transaction(): add a transaction
3. update_transaction(): update a transaction
4. delete_transaction(): delete a transaction
"""
import ipywidgets as widgets
import qgrid
import pandas as pd


def display_transaction(project_name):
    """
    :param project_name: the name of the project
    :return: a qgrid table widget to show the dataframe as a table
    """
    df = pd.read_json('./data/{0}.json'.format(project_name), orient='records')
    df.set_index("id", inplace=True)
    df["Category"] = df["Category"].astype("category")
    df['Date'] = pd.to_datetime(df['Date'], unit='s')
    df["Amount"] = df["Amount"].astype('float64')
    qgrid_widget = qgrid.show_grid(df)
    return qgrid_widget


def date_widget():
    """
    :return: widget to enter the date
    """
    print('Please pick the date of the transaction: ')
    date = widgets.DatePicker(
        description='Date:',
        disabled=False
    )
    return date


def amount_widget(date):
    """
    :param date: the date input widget, to validate the value
    :return: widget to enter the amount
    """
    print('The date is: {0}'.format(date.value))
    print('Please enter the amount of the transaction: ')
    amount = widgets.BoundedFloatText(
        min=0,
        max=1000000,
        step=0.01,
        description='Amount:',
        disabled=False
    )
    return amount


def category_widget(amount):
    """
    :param amount: the amount input widget, to validate the value
    :return: widget to enter the category
    """
    print('The amount is: {0}'.format(amount.value))
    print('Please choose the category of the transaction: ')
    category = widgets.Dropdown(
        options=['Home & Utilities', 'Transportation',
                 'Groceries', 'Restaurants & Dining',
                 'Shopping & Entertainment',
                 'Education', 'Health', 'Others'],
        description='Category:',
        disabled=False,
    )
    return category


def account_widget(category):
    """
    :param category: the category input widget, to validate the value
    :return: widget to enter the account
    """
    print('The category is: {0}'.format(category.value))
    print('Please choose the account of the transaction: ')
    account = widgets.Dropdown(
        options=['Cash', 'Debit Card', 'Credit Card'],
        description='Account:',
        disabled=False,
    )
    return account


def description_widget(account):
    """
    :param account: the account input widget, to validate the value
    :return: widget to enter the description
    """
    print('The account is: {0}'.format(account.value))
    print('Please enter the description of the transaction: ')
    description = widgets.Text(
        description='Description:',
        disabled=False
    )
    return description


def get_id_list(project_name):
    """
    :param project_name: the name of the project
    :return: the list of all the transaction's id
    """
    df = pd.read_json('./data/{0}.json'.format(project_name), orient='record')
    id_list = df['id'].tolist()
    return id_list


def set_id(description, project_name):
    """
    :param description: the description input widget, to validate the value
    :param project_name: the name of the project
    :return: the id of the transaction to add
    """
    print('The description is: {0}'.format(description.value))
    id_list = get_id_list(project_name)
    id = id_list[-1] + 1
    print('The id is: {0}'.format(id))
    return id


def confirm_add(id, date, amount, category, account, description,
                project_name):
    """
    :return: a widget to confirm the id to add
    """
    if id in get_id_list(project_name):
        print('This id already exists in the project, please check')
    else:
        ds = pd.Series({'id': id, 'Date': date.value, 'Amount': amount.value,
                        'Category': str(category.value),
                        'Account': str(account.value),
                        'Description': str(description.value)})
        print('\nThe transaction to add: ')
        display(ds)
        check_add_widget = widgets.Checkbox(
            value=False,
            description='Yes, add',
            disabled=False,
            indent=False
        )
        print('Do you want to add the transaction? ')
        return check_add_widget


def add_transaction(id, date, amount, category, account, description,
                    project_name, add_checker):
    """
    if the add transaction is confirmed, add the new transaction data
    """
    if add_checker.value:
        df = pd.read_json('./data/{0}.json'.format(project_name),
                          orient='record')
        df = df.append({'id': id, 'Date': date.value, 'Amount': amount.value,
                        'Category': str(category.value),
                        'Account': str(account.value),
                        'Description': str(description.value)},
                       ignore_index=True)
        df.to_json('./data/{0}.json'.format(project_name), orient='records')
        print('The transaction is added')
    else:
        print('The add failed, you need to confirm first')


def get_id_to_update(project_name):
    """
    :param project_name: the name of the project
    :return: a widget to select the id of the transaction to update
    """
    if not get_id_list(project_name):
        print('There is no transaction to update')
    else:
        id_list = get_id_list(project_name)
        new_list = []
        for item in id_list:
            new_list.append(str(item))
        print('Please enter the id of the transaction you want to update:')
        id_widget = widgets.Combobox(
            placeholder='Choose',
            options=new_list,
            description='id:',
            ensure_option=True,
            disabled=False
        )
        return id_widget


def confirm_update(id, date, amount, category, account, description,
                   project_name):
    """
    :return: a check widget to confirm the update
    """
    if id not in get_id_list(project_name):
        print('This id does not exist, please check')
    else:
        df = pd.read_json('./data/{0}.json'.format(project_name),
                          orient='record')
        ds = df.loc[df['id'] == id].squeeze()
        print('The original transaction information: ')
        display(ds)
        ds_new = pd.Series({'id': id, 'Date': date, 'Amount': amount,
                            'Category': category, 'Account': account,
                            'Description': description})
        print('\nThe updated transaction information: ')
        display(ds_new)
        check_update_widget = widgets.Checkbox(
            value=False,
            description='Yes, update',
            disabled=False,
            indent=False
        )
        print('Do you want to update the transaction? ')
        return check_update_widget


def update_transaction(id, date, amount, category, account, description,
                       project_name, update_checker):
    """
    once confirmed, replace the transaction value with the new one
    """
    if update_checker.value:
        df = pd.read_json('./data/{0}.json'.format(project_name),
                          orient='record')
        df.loc[df['id'] == id, 'Date'] = date
        df.loc[df['id'] == id, 'Amount'] = amount
        df.loc[df['id'] == id, 'Category'] = category
        df.loc[df['id'] == id, 'Account'] = account
        df.loc[df['id'] == id, 'Description'] = description
        df.to_json('./data/{0}.json'.format(project_name), orient='records')
        print('The transaction is updated')
    else:
        print('The update failed, you need to confirm first')


def get_id_to_delete(project_name):
    """
    :return: a widget to select the id to delete
    """
    if not get_id_list(project_name):
        print('There is no transaction to delete')
    else:
        id_list = get_id_list(project_name)
        new_list = []
        for item in id_list:
            new_list.append(str(item))
        print('Please enter the id of the transaction that you want to '
              'delete:')
        id_widget = widgets.Combobox(
            placeholder='Choose',
            options=new_list,
            description='id:',
            ensure_option=True,
            disabled=False
        )
        return id_widget


def confirm_delete(id, project_name):
    """
    :return: a checker widget to confirm the delete
    """
    if id not in get_id_list(project_name):
        print('This id does not exist, please check')
    elif id == 0:
        print('This is the initial value, which can not be deleted')
    else:
        df = pd.read_json('./data/{0}.json'.format(project_name),
                          orient='record')
        ds = df.loc[df['id'] == id].squeeze()
        print('The  transaction information: ')
        display(ds)
        check_delete_widget = widgets.Checkbox(
            value=False,
            description='Yes, delete',
            disabled=False,
            indent=False
        )
        print('Do you want to delete the transaction? ')
        return check_delete_widget


def delete_transaction(id, project_name, delete_checker):
    """
    once confirmed, delete the transaction
    """
    if delete_checker.value:
        df = pd.read_json('./data/{0}.json'.format(project_name),
                          orient='record')
        df = df[df['id'] != id]
        df.to_json('./data/{0}.json'.format(project_name), orient='records')
        print('The transaction is deleted')
    else:
        print('The delete failed, you need to confirm first')
