import pytest

from models.customer import CreateCustomer
from pages.try_sql_page import TrySQLPage, TrySQLPageResultColumn
from utils.constants.routes import UIRoutes


class TestW3SchoolsSQL:
    @pytest.mark.parametrize('text', ['Via Ludovico il Moro 22'])
    @pytest.mark.parametrize('reference_text', ['Via Ludovico il Moro 22'])
    def test_select_all_customers(self, try_sql_page: TrySQLPage, text: str, reference_text: str):
        try_sql_page.visit(f'{UIRoutes.SQL_TRYSQL}?filename=trysql_select_all')
        try_sql_page.fill_sql_editor('SELECT * FROM Customers;')
        try_sql_page.run_sql()
        try_sql_page.check_result_table_data(
            expected_text=text,
            reference_text=reference_text,
            column=TrySQLPageResultColumn.ADDRESS
        )

    @pytest.mark.parametrize('number_of_records', [6])
    def test_filter_customers(self, try_sql_page: TrySQLPage, number_of_records: int):
        try_sql_page.visit(f'{UIRoutes.SQL_TRYSQL}?filename=trysql_select_all')
        try_sql_page.fill_sql_editor(
            'SELECT * FROM Customers WHERE City="London";'
        )
        try_sql_page.run_sql()
        try_sql_page.check_number_of_records(number_of_records)

    @pytest.mark.parametrize('create_customer', [CreateCustomer.get_random(),])
    def test_create_customer(self, try_sql_page: TrySQLPage, create_customer: CreateCustomer):
        try_sql_page.visit(f'{UIRoutes.SQL_TRYSQL}?filename=trysql_select_all')
        try_sql_page.fill_sql_editor(
            f"INSERT INTO Customers {create_customer.columns()} VALUES {create_customer.values()};"
        )
        try_sql_page.run_sql(insert_rows=1)

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
