import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'screens/splash_screen.dart';
import 'screens/login_screen.dart';
import 'screens/player_dashboard.dart';
import 'screens/upload_screen.dart';
import 'screens/reports_screen.dart';
import 'screens/coach_chat_screen.dart';
import 'screens/scout_discover_screen.dart';
import 'screens/leaderboard_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/notifications_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );
  runApp(const AlLaeebApp());
}

class AlLaeebApp extends StatelessWidget {
  const AlLaeebApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Al-La'eeb",
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0A0E21),
        cardColor: const Color(0xFF1D1F33),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00B894),
          secondary: Color(0xFF0984E3),
          surface: Color(0xFF1D1F33),
          background: Color(0xFF0A0E21),
          error: Color(0xFFFF6B6B),
          onPrimary: Colors.white,
          onSecondary: Colors.white,
        ),
        textTheme: const TextTheme(
          displayLarge: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
          displayMedium: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
          titleLarge: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.w600),
          titleMedium: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w500),
          bodyLarge: TextStyle(color: Colors.white, fontSize: 16),
          bodyMedium: TextStyle(color: Colors.white70, fontSize: 14),
          bodySmall: TextStyle(color: Colors.white54, fontSize: 12),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0A0E21),
          elevation: 0,
          centerTitle: true,
          titleTextStyle: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
        ),
        bottomNavigationBarTheme: const BottomNavigationBarThemeData(
          backgroundColor: Color(0xFF1D1F33),
          selectedItemColor: Color(0xFF00B894),
          unselectedItemColor: Colors.white38,
          type: BottomNavigationBarType.fixed,
          elevation: 8,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF00B894),
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            elevation: 0,
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: const Color(0xFF1D1F33),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: Color(0xFF00B894), width: 2),
          ),
          labelStyle: const TextStyle(color: Colors.white70),
          hintStyle: const TextStyle(color: Colors.white38),
        ),
        cardTheme: CardTheme(
          color: const Color(0xFF1D1F33),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          elevation: 0,
        ),
      ),
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('en'),
        Locale('ar'),
      ],
      initialRoute: '/',
      routes: {
        '/': (context) => const SplashScreen(),
        '/login': (context) => const LoginScreen(),
        '/dashboard': (context) => const PlayerDashboard(),
        '/upload': (context) => const UploadScreen(),
        '/reports': (context) => const ReportsScreen(),
        '/coach': (context) => const CoachChatScreen(),
        '/discover': (context) => const ScoutDiscoverScreen(),
        '/leaderboard': (context) => const LeaderboardScreen(),
        '/profile': (context) => const ProfileScreen(),
        '/notifications': (context) => const NotificationsScreen(),
      },
    );
  }
}
