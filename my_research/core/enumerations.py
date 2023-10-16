from my_research.utils.enumeration import Enumeration


class UserRoles(Enumeration):
    user = "user"
    employee = "employee"
    dev = "dev"

    def set():
        return {"user", "employee", "dev"}


class ResearchTypes(Enumeration):
    lw = "lw"
    research = "research"

    def set():
        return {"lw", "research"}


class MailCodeTypes(Enumeration):
    reg = "reg"
    auth = "auth"