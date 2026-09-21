class User {
  final String id;
  final String email;
  final String firstName;
  final String lastName;
  final String role;
  final bool isVerified;

  User({
    required this.id,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.role,
    required this.isVerified,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json["id"],
      email: json["email"],
      firstName: json["first_name"],
      lastName: json["last_name"],
      role: json["role"],
      isVerified: json["is_verified"],
    );
  }
}
