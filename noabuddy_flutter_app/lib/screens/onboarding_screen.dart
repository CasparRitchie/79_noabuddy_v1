// import 'package:flutter/material.dart';

// class OnboardingScreen extends StatefulWidget {
//   const OnboardingScreen({Key? key}) : super(key: key);

//   @override
//   State<OnboardingScreen> createState() => _OnboardingScreenState();
// }

// class _OnboardingScreenState extends State<OnboardingScreen> {
//   int _currentPage = 0;
//   final PageController _controller = PageController();

//   final List<Widget> _pages = [
//     _OnboardPage(
//       title: "Welcome to NoaBuddy",
//       subtitle: "Helping you connect when you need it most.",
//       buttonText: "Next",
//     ),
//     _OnboardPage(
//       title: "How NoaBuddy works...",
//       subtitle: "Your private, judgment-free relationship assistant.",
//       buttonText: "Next",
//     ),
//     _OnboardPage(
//       title: "Choose your Privacy...",
//       subtitle: "Save or delete conversations after each session.",
//       buttonText: "Next",
//     ),
//     _OnboardPage(
//       title: "Ready?",
//       subtitle: "Let's get started.",
//       buttonText: "Continue",
//     ),
//   ];

//   void _nextPage() {
//     if (_currentPage < _pages.length - 1) {
//       _controller.nextPage(duration: Duration(milliseconds: 300), curve: Curves.easeInOut);
//     } else {
//       // TODO: Navigate to ChatScreen
//       print("Navigate to chat screen");
//     }
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: Stack(
//         children: [
//           PageView.builder(
//             controller: _controller,
//             itemCount: _pages.length,
//             onPageChanged: (index) => setState(() => _currentPage = index),
//             itemBuilder: (_, index) => _pages[index],
//           ),
//           Positioned(
//             bottom: 20,
//             left: 0,
//             right: 0,
//             child: Center(
//               child: Row(
//                 mainAxisAlignment: MainAxisAlignment.center,
//                 children: List.generate(
//                   _pages.length,
//                   (index) => AnimatedContainer(
//                     duration: Duration(milliseconds: 300),
//                     margin: EdgeInsets.symmetric(horizontal: 5),
//                     width: _currentPage == index ? 12 : 8,
//                     height: 8,
//                     decoration: BoxDecoration(
//                       color: _currentPage == index ? Colors.black : Colors.grey,
//                       borderRadius: BorderRadius.circular(4),
//                     ),
//                   ),
//                 ),
//               ),
//             ),
//           ),
//         ],
//       ),
//     );
//   }
// }

// class _OnboardPage extends StatelessWidget {
//   final String title;
//   final String subtitle;
//   final String buttonText;

//   const _OnboardPage({
//     required this.title,
//     required this.subtitle,
//     required this.buttonText,
//   });

//   @override
//   Widget build(BuildContext context) {
//     return Padding(
//       padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 60.0),
//       child: Column(
//         mainAxisAlignment: MainAxisAlignment.center,
//         children: [
//           Spacer(),
//           Icon(Icons.favorite, size: 100, color: Colors.teal), // Placeholder icon
//           SizedBox(height: 32),
//           Text(
//             title,
//             textAlign: TextAlign.center,
//             style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
//           ),
//           SizedBox(height: 16),
//           Text(
//             subtitle,
//             textAlign: TextAlign.center,
//             style: TextStyle(fontSize: 16),
//           ),
//           Spacer(),
//           ElevatedButton(
//             onPressed: () => Navigator.of(context).maybePop(),
//             style: ElevatedButton.styleFrom(
//               backgroundColor: Colors.black,
//               shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
//               padding: EdgeInsets.symmetric(horizontal: 40, vertical: 14),
//             ),
//             child: Text(buttonText, style: TextStyle(fontSize: 16)),
//           ),
//         ],
//       ),
//     );
//   }
// }


import 'package:flutter/material.dart';
import 'chat_screen.dart';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({Key? key}) : super(key: key);

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  final PageController _controller = PageController();
  int _currentPage = 0;

  final List<_OnboardContent> _pages = [
    _OnboardContent(
      backgroundImage: 'assets/images/onboarding_bg.png',
      logo: 'assets/images/noabuddy_logo.png',
      title: "Welcome to NoaBuddy",
      subtitle: "Helping you connect when you need it most.",
      buttonText: "Next",
    ),
    _OnboardContent(
      logo: 'assets/images/noabuddy_logo.png',
      title: "How NoaBuddy works...",
      subtitle:
          "Acting as your relationship companion, NoaBuddy uses proven therapy practices to help couples navigate their relationships in real time.",
      buttonText: "Next",
    ),
    _OnboardContent(
      logo: 'assets/images/noabuddy_logo.png',
      title: "Choose your Privacy...",
      subtitle:
          "Save conversations to learn and improve,\nor delete chats after each session.",
      buttonText: "Next",
    ),
    _OnboardContent(
      logo: 'assets/images/noabuddy_logo.png',
      title: "Noa Buddy",
      subtitle: "Ready?",
      buttonText: "Let’s get started",
      isFinal: true,
    ),
  ];

  void _nextPage() {
    if (_currentPage < _pages.length - 1) {
      _controller.nextPage(duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const ChatScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          PageView.builder(
            controller: _controller,
            itemCount: _pages.length,
            onPageChanged: (index) => setState(() => _currentPage = index),
            itemBuilder: (_, index) => _pages[index].buildPage(context, _nextPage),
          ),
          Positioned(
            bottom: 30,
            left: 0,
            right: 0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(_pages.length, (index) {
                return AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  margin: const EdgeInsets.symmetric(horizontal: 4),
                  width: _currentPage == index ? 12 : 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: _currentPage == index ? Colors.black : Colors.grey[400],
                    borderRadius: BorderRadius.circular(4),
                  ),
                );
              }),
            ),
          )
        ],
      ),
    );
  }
}

class _OnboardContent {
  final String? backgroundImage;
  final String logo;
  final String title;
  final String subtitle;
  final String buttonText;
  final bool isFinal;

  _OnboardContent({
    this.backgroundImage,
    required this.logo,
    required this.title,
    required this.subtitle,
    required this.buttonText,
    this.isFinal = false,
  });

  Widget buildPage(BuildContext context, VoidCallback onNext) {
    return Stack(
      children: [
        if (backgroundImage != null)
          Positioned.fill(
            child: Image.asset(
              backgroundImage!,
              fit: BoxFit.cover,
            ),
          ),
        Positioned.fill(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 32),
            decoration: BoxDecoration(
              color: backgroundImage != null ? Colors.black.withOpacity(0.3) : Colors.white,
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Spacer(),
                Image.asset(logo, width: 100, height: 100),
                const SizedBox(height: 32),
                Text(
                  title,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                    color: backgroundImage != null ? Colors.white : Colors.black,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  subtitle,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 16,
                    color: backgroundImage != null ? Colors.white70 : Colors.black87,
                  ),
                ),
                const Spacer(),
                ElevatedButton(
                  onPressed: onNext,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.black,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                  ),
                  child: Text(buttonText),
                ),
                const SizedBox(height: 40),
              ],
            ),
          ),
        )
      ],
    );
  }
}
