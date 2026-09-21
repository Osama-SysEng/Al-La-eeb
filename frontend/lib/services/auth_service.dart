import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  static const String baseUrl = "https://api.allaeeb.com/api/v1";
  static const _storage = FlutterSecureStorage();

  Future<void> login(String email, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/login"),
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: {"username": email, "password": password},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await _storage.write(key: "access_token", value: data["access_token"]);
      await _storage.write(key: "refresh_token", value: data["refresh_token"]);
    } else {
      throw Exception("Login failed: ${response.body}");
    }
  }

  Future<void> logout() async {
    await _storage.deleteAll();
  }

  Future<String?> getToken() async {
    return await _storage.read(key: "access_token");
  }
}
