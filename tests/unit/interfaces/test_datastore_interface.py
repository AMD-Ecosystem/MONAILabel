# Copyright (c) MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from monailabel.interfaces.datastore import Datastore


class _ConcreteDatastore(Datastore):
    # Implement every abstract method by delegating to super() so the base-class
    # (abstract) method bodies execute for coverage. Bodies are `pass` -> None.
    def name(self):
        return super().name()

    def set_name(self, name):
        return super().set_name(name)

    def description(self):
        return super().description()

    def set_description(self, description):
        return super().set_description(description)

    def datalist(self):
        return super().datalist()

    def get_labels_by_image_id(self, image_id):
        return super().get_labels_by_image_id(image_id)

    def get_label_by_image_id(self, image_id, tag):
        return super().get_label_by_image_id(image_id, tag)

    def get_image(self, image_id, params=None):
        return super().get_image(image_id, params)

    def get_image_uri(self, image_id):
        return super().get_image_uri(image_id)

    def get_label(self, label_id, label_tag, params=None):
        return super().get_label(label_id, label_tag, params)

    def get_label_uri(self, label_id, label_tag):
        return super().get_label_uri(label_id, label_tag)

    def get_image_info(self, image_id):
        return super().get_image_info(image_id)

    def get_label_info(self, label_id, label_tag):
        return super().get_label_info(label_id, label_tag)

    def get_labeled_images(self, label_tag=None, labels=None):
        return super().get_labeled_images(label_tag, labels)

    def get_unlabeled_images(self, label_tag=None, labels=None):
        return super().get_unlabeled_images(label_tag, labels)

    def list_images(self):
        return super().list_images()

    def get_dataset_archive(self, limit_cases):
        return super().get_dataset_archive(limit_cases)

    def refresh(self):
        return super().refresh()

    def add_image(self, image_id, image_filename, image_info):
        return super().add_image(image_id, image_filename, image_info)

    def remove_image(self, image_id):
        return super().remove_image(image_id)

    def save_label(self, image_id, label_filename, label_tag, label_info):
        return super().save_label(image_id, label_filename, label_tag, label_info)

    def remove_label(self, label_id, label_tag):
        return super().remove_label(label_id, label_tag)

    def update_image_info(self, image_id, info):
        return super().update_image_info(image_id, info)

    def update_label_info(self, label_id, label_tag, info):
        return super().update_label_info(label_id, label_tag, info)

    def status(self):
        return super().status()

    def json(self):
        return super().json()


class TestDatastoreInterface(unittest.TestCase):
    def test_abstract_bodies_execute(self):
        ds = _ConcreteDatastore()
        # Each call executes the base-class abstract method body (pass -> None)
        self.assertIsNone(ds.name())
        self.assertIsNone(ds.set_name("n"))
        self.assertIsNone(ds.description())
        self.assertIsNone(ds.set_description("d"))
        self.assertIsNone(ds.datalist())
        self.assertIsNone(ds.get_labels_by_image_id("i"))
        self.assertIsNone(ds.get_label_by_image_id("i", "t"))
        self.assertIsNone(ds.get_image("i"))
        self.assertIsNone(ds.get_image_uri("i"))
        self.assertIsNone(ds.get_label("l", "t"))
        self.assertIsNone(ds.get_label_uri("l", "t"))
        self.assertIsNone(ds.get_image_info("i"))
        self.assertIsNone(ds.get_label_info("l", "t"))
        self.assertIsNone(ds.get_labeled_images())
        self.assertIsNone(ds.get_unlabeled_images())
        self.assertIsNone(ds.list_images())
        self.assertIsNone(ds.get_dataset_archive(None))
        self.assertIsNone(ds.refresh())
        self.assertIsNone(ds.add_image("i", "f", {}))
        self.assertIsNone(ds.remove_image("i"))
        self.assertIsNone(ds.save_label("i", "f", "t", {}))
        self.assertIsNone(ds.remove_label("l", "t"))
        self.assertIsNone(ds.update_image_info("i", {}))
        self.assertIsNone(ds.update_label_info("l", "t", {}))
        self.assertIsNone(ds.status())
        self.assertIsNone(ds.json())


if __name__ == "__main__":
    unittest.main()
