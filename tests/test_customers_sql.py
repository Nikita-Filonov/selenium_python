import allure
import pytest

from models.customer import CreateCustomer
from pages.try_sql_page import TrySQLPage, TrySQLPageResultColumn
from utils.constants.features import Feature
from utils.constants.routes import UIRoutes
from utils.constants.suites import Suite


@pytest.mark.ui
@pytest.mark.customers_sql
@allure.severity(allure.severity_level.CRITICAL)
@allure.suite(Suite.SMOKE)
@allure.feature(Feature.CUSTOMERS)
class TestCustomersSQL:
    SQL_TRYSQL_URL = f'{UIRoutes.SQL_TRYSQL}?filename=trysql_select_all'

    @allure.id('1')
    @allure.title('Select all customers')
    @pytest.mark.parametrize('text', ['Via Ludovico il Moro 22'])
    @pytest.mark.parametrize('reference_text', ['Via Ludovico il Moro 22'])
    def test_select_all_customers(self, try_sql_page: TrySQLPage, text: str, reference_text: str):
        try_sql_page.visit(self.SQL_TRYSQL_URL)
        try_sql_page.fill_sql_editor('SELECT * FROM Customers;')
        try_sql_page.run_sql()
        try_sql_page.check_result_table_data(
            expected_text=text,
            reference_text=reference_text,
            column=TrySQLPageResultColumn.ADDRESS
        )

    @allure.id('2')
    @allure.title('Filter customers')
    @pytest.mark.parametrize('number_of_records', [6])
    def test_filter_customers(self, try_sql_page: TrySQLPage, number_of_records: int):
        try_sql_page.visit(self.SQL_TRYSQL_URL)
        try_sql_page.fill_sql_editor(
            'SELECT * FROM Customers WHERE City="London";'
        )
        try_sql_page.run_sql()
        try_sql_page.check_number_of_records(number_of_records)

    @allure.id('3')
    @allure.title('Create customer')
    @pytest.mark.parametrize('create_customer', [CreateCustomer.get_random()])
    def test_create_customer(self, try_sql_page: TrySQLPage, create_customer: CreateCustomer):
        try_sql_page.visit(self.SQL_TRYSQL_URL)
        try_sql_page.fill_sql_editor(
            f'INSERT INTO Customers {create_customer.columns()} VALUES {create_customer.values()};'
        )
        try_sql_page.run_sql(rows_affected=1)

        try_sql_page.fill_sql_editor(
            f'SELECT * FROM Customers WHERE CustomerName="{create_customer.customer_name}";'
        )
        try_sql_page.run_sql()
        try_sql_page.check_result_table_row(
            expected_texts=create_customer.values(),
            reference_text=create_customer.customer_name,
            columns=TrySQLPageResultColumn.to_list(
                exclude=[TrySQLPageResultColumn.CUSTOMER_ID]
            )
        )

    @allure.id('4')
    @allure.title('Update customer')
    @pytest.mark.parametrize('customer_id', ['1'])
    @pytest.mark.parametrize('update_customer', [CreateCustomer.get_random()])
    def test_update_customer(
        self,
        try_sql_page: TrySQLPage,
        customer_id: str,
        update_customer: CreateCustomer,
    ):
        try_sql_page.visit(self.SQL_TRYSQL_URL)
        try_sql_page.fill_sql_editor(
            f'UPDATE Customers SET {update_customer.join_values()} WHERE CustomerID={customer_id};'
        )
        try_sql_page.run_sql(rows_affected=1)

        try_sql_page.fill_sql_editor(
            f'SELECT * FROM Customers WHERE CustomerID="{customer_id}";'
        )
        try_sql_page.run_sql()
        try_sql_page.check_result_table_row(
            expected_texts=(customer_id, *update_customer.values()),
            reference_text=customer_id,
            columns=TrySQLPageResultColumn.to_list()
        )

    @allure.id('5')
    @allure.title('Delete customer')
    @pytest.mark.parametrize('customer_id', ['1'])
    def test_delete_customer(self, try_sql_page: TrySQLPage, customer_id: str):
        try_sql_page.visit(self.SQL_TRYSQL_URL)
        try_sql_page.fill_sql_editor(
            f'DELETE FROM Customers WHERE CustomerID="{customer_id}";'
        )
        try_sql_page.run_sql(rows_affected=1)

        try_sql_page.fill_sql_editor(
            f'SELECT * FROM Customers WHERE CustomerID="{customer_id}";'
        )
        try_sql_page.run_sql(empty_result=True)
