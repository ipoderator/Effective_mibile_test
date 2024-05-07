import unittest
from unittest.mock import patch, mock_open
import csv
from click.testing import CliRunner

from add_data import transaction_data
from constants import MY_DATE, TESTING, RECORDS
from main import add_record, view_balance, write_data, search_record


class TestWalletFunctions(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            TESTING[0],
            TESTING[1],
            TESTING[2]
        ]
        self.test_file_name = 'test_transactions.csv'

    def tearDown(self):
        transaction_data.clear()

    def test_write_data(self):
        with patch('builtins.open', mock_open()) as mock_file:
            write_data(self.test_file_name, self.test_data, 'w')
            mock_file.assert_called_with(
                self.test_file_name, 'w', newline='', encoding='utf-8'
            )

    def test_view_balance(self):
        transaction_data.extend(self.test_data)
        runner = CliRunner()
        result = runner.invoke(view_balance)
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Текущий баланс: 2500', result.output)
        self.assertIn('Доходы: 3000', result.output)
        self.assertIn('Расходы: 500', result.output)

    def test_search_record(self):
        transaction_data.extend(self.test_data)
        runner = CliRunner()
        with runner.isolated_filesystem():
            with patch('click.prompt', side_effect=['Категория', 'Доход']):
                result = runner.invoke(search_record)
                self.assertEqual(result.exit_code, 0)
                self.assertIn('Найденные записи:', result.output)
                self.assertIn(f"{RECORDS[0]}", result.output)
                self.assertIn(f"{RECORDS[1]}", result.output)

    def test_add_record(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with patch('click.prompt', side_effect=['Доход']):
                with patch('builtins.input',
                           side_effect=['1000', 'Новый доход']):
                    result = runner.invoke(add_record, [self.test_file_name])
                    self.assertEqual(result.exit_code, 0)
                    expected_output = (
                        f"Дата: {MY_DATE.strftime('%Y-%m-%d')}\n"
                        f"Категория: Доход\n"
                        f"Сумма: 1000\n"
                        f"Описание: Новый доход"
                    )
                    self.assertIn(expected_output, result.output)

                    with open(self.test_file_name, 'r', newline='',
                              encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        records = list(reader)
                        self.assertEqual(len(records), 0)
                        expected_record = {
                            'Дата': MY_DATE.strftime("%Y-%m-%d"),
                            'Категория': 'Доход',
                            'Сумма': '1000',
                            'Описание': 'Новый доход'
                        }
                        return expected_record


if __name__ == '__main__':
    unittest.main()
