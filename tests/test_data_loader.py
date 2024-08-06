import os
import pytest
from unittest.mock import Mock, patch
from src.common import Parser
from src.data_loader import YOLOv8DataLoader

# Fixtures
@pytest.fixture
def mock_parser():
    mock = Mock(spec=Parser)
    mock.get_data.return_value = ['data1', 'data2']
    mock.malformed_lines_count = 0
    return mock

@pytest.fixture
def data_loader(tmp_path, mock_parser):
    labels_dir = tmp_path / "labels"
    labels_dir.mkdir()
    for i in range(3):
        (labels_dir / f"treatment_rep_{i}.txt").write_text("some text content")

    return YOLOv8DataLoader(labels_dir=str(labels_dir), parser=mock_parser)

# Tests
def test_extract_treatment_rep_frame(data_loader):
    treatment, rep, frame = data_loader.extract_treatment_rep_frame("treatment_rep_1.txt")
    assert treatment == "treatment"
    assert rep == "rep"
    assert frame == "1"

@patch('src.data_loader.Parser', autospec=True)
def test_process_file(mock_parser_class, data_loader, mock_parser):
    mock_parser_instance = mock_parser_class.return_value
    mock_parser_instance.get_data.return_value = ['data1', 'data2']
    mock_parser_instance.malformed_lines_count = 1

    data, malformed_count = data_loader.process_file("treatment_rep_1.txt")

    assert data == ['data1', 'data2']
    assert malformed_count == 1
    mock_parser_class.assert_called_once()
    mock_parser_instance.parse_file.assert_called_once()

@patch('src.data_loader.concurrent.futures.ProcessPoolExecutor', autospec=True)
def test_load_data(mock_executor, data_loader, mock_parser):
    mock_future = Mock()
    mock_future.result.return_value = (['data1', 'data2'], 0)

    mock_executor_instance = mock_executor.return_value
    mock_executor_instance.__enter__.return_value.submit.side_effect = [
        mock_future, mock_future, mock_future
    ]

    data_loader.load_data(samples=2)

    assert len(data_loader.get_data()) == 6
    assert data_loader.malformed_lines_count == 0
    assert mock_executor_instance.submit.call_count == 2

if __name__ == '__main__':
    pytest.main()
