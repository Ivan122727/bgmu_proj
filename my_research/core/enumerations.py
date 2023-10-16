from my_research.utils.enumeration import Enumeration


class UserRoles(Enumeration):
    user = "user"
    employee = "employee"
    dev = "dev"

    def set():
        return {"user", "employee", "dev"}


class ResearchTypes(Enumeration):
    img = "img"
    file = "file"

    def set():
        return {"img", "file"}


class MailCodeTypes(Enumeration):
    reg = "reg"
    auth = "auth"