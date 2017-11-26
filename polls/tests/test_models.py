import pytest
from unittest.mock import patch

from django.test import TestCase

from polls.models import Video  # , VideoFolder
from polls.exceptions import AliasesContainSpaces, FolderContainsNoVideos, InvalidPath
from .factories import VideoFolderFactory


@pytest.mark.django_db
class TestVideoFolderModel(TestCase):
    def test_raises_if_spaces_in_aliases(self):
            with self.assertRaises(AliasesContainSpaces):
                VideoFolderFactory(aliases='test testy')

    def test_raises_if_invalid_path(self):
        with patch('polls.models.os.path.isdir', return_value=False):
            with self.assertRaises(InvalidPath):
                VideoFolderFactory()

    def test_creates_videos(self):
        with patch('polls.models.os.path.isdir', return_value=True):
            with patch('polls.models.os.listdir', return_value=['test.avi', 'readme.txt', 'test2.mp4']):
                folder = VideoFolderFactory()
                videos = Video.objects.filter(folder=folder)
                assert videos.count() == 2
                assert videos.filter(last_played=None).count() == 2
                assert set(v.file_name for v in videos) == set(['test.avi', 'test2.mp4'])


class TestVideoModel(TestCase):
    def test_is_video_file(self):
        assert Video.is_video_file("test.mp4")
        assert Video.is_video_file("test.MP4")
        assert Video.is_video_file("test.avi")
        assert not Video.is_video_file("test.txt")
        assert not Video.is_video_file("testavi")
