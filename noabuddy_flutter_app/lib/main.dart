import 'package:flutter/material.dart';
import 'screens/chat_screen.dart';


void main() {
  runApp(const NoaBuddyApp());
}

class NoaBuddyApp extends StatelessWidget {
  const NoaBuddyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'NoaBuddy',
      theme: ThemeData(
        primarySwatch: Colors.teal,
        scaffoldBackgroundColor: Colors.white,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.teal,
          foregroundColor: Colors.white,
          elevation: 1,
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
        ),
      ),
      home: const ChatScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
