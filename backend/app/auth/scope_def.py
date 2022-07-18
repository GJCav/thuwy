from .model import Scope

BasicUser = Scope.define("User", "Basic user permission", True)
ScopeAdmin = Scope.define("ScopeAdmin", "Admin for permission", True)
UserAdmin = Scope.define("UserAdmin", "Admin for all users", True)