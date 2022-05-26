import discord
import json


class RoleLink(object):
    def __init__(self, role, link):
        self.role = role
        self.role_id = role.id
        self.link = link

    def get_role(self):
        return self.role

    def get_link(self):
        return self.link

    def as_dict(self):
        return {'role_id': self.role_id, 'link': self.link}
