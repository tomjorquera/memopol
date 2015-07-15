# coding: utf-8

# This file is part of memopol.
#
# memopol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# memopol is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>
from __future__ import absolute_import


def create_child_instance_from_parent(child_cls, parent_instance):
    """
    Create a child model instance from a parent instance
    """
    parent_cls = parent_instance.__class__
    field = child_cls._meta.get_ancestor_link(parent_cls).column

    child_instance = child_cls(**{
        field: parent_instance.pk
    })

    child_instance.__dict__.update(parent_instance.__dict__)
    child_instance.save()
    return child_instance