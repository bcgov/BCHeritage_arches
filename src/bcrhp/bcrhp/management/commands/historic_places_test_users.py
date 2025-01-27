"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import uuid
from arches.management.commands import utils
from arches.app.models import models
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from test_users import BCHP_TEST_USERS


class Command(BaseCommand):
    """
    Commands for adding arches test users

    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            default=False,
            help="refresh users. delete existing users if they exist",
        )
        parser.add_argument(
            "--delete", default=False, help="delete historic places test users"
        )
        parser.add_argument(
            "--add", default=False, help="add historic places test users"
        )

    def handle(self, *args, **options):
        print(options["refresh"])
        if options["refresh"] or options["delete"]:
            self.delete_users()
        else:
            print("Not trying to delete users")

        if options["refresh"] or options["add"]:
            self.add_users()
        else:
            print("Not trying to add users")

    def get_profiles(self):
        return BCHP_TEST_USERS

    def delete_users(self):
        profiles = self.get_profiles()
        for profile in profiles:
            try:
                user = User.objects.get(username=profile["name"])
                if user is not None:
                    user.delete()
                    print("Deleted user " + str(user))
            except Exception:
                print("User " + profile["name"] + " does not exist")

    def add_users(self):
        profiles = self.get_profiles()

        for profile in profiles:
            try:
                user = User.objects.create_user(
                    username=profile["name"],
                    email=profile["email"],
                    password=profile["password"],
                    is_superuser=(
                        profile["is_superuser"] if "is_superuser" in profile else False
                    ),
                    is_staff=profile["is_staff"] if "is_staff" in profile else False,
                    first_name=(
                        profile["first_name"]
                        if "first_name" in profile
                        else profile["name"]
                    ),
                    last_name=(
                        profile["last_name"]
                        if "last_name" in profile
                        else profile["name"]
                    ),
                )
                user.save()

                print(
                    f"Added test user: {user.username}"
                )

                for group_name in profile["groups"]:
                    group = Group.objects.get_or_create(name=group_name)
                    print("\tGot group: " + str(group[0].name))
                    if group[1]:
                        print(f"\t\tCreated new group {group[0].name}")
                    group[0].user_set.add(user)

            except Exception as e:
                print("Exception: " + str(e))
