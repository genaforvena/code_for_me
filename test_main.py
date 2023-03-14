from unittest import TestCase, mock

from main import predict, message_history, read_file


class TestPredict(TestCase):
    @mock.patch('openai.ChatCompletion.create')
    def test_predict(self, mock_create):
        mock_create.return_value.choices[0].message.content = "Hello, how can I help you today?"

        predict("Hi")
        self.assertEqual(len(message_history), 6)
        self.assertEqual(message_history[-1]["content"], "Hello, how can I help you today?")

    def test_read_file(self):
        # Test with a file that exists and is readable
        expected_contents = "Here is my code:\n```print('Hello, World!')```" \
                            "\n Please read it and explain what it does."
        actual_contents = read_file("assets/hello_world.py")
        self.assertEqual(actual_contents, expected_contents)

        # Test with a file that does not exist
        actual_contents = read_file("non_existent_file")
        self.assertIsNone(actual_contents)