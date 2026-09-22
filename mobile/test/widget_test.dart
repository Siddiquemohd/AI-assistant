import 'package:flutter_test/flutter_test.dart';
import 'package:isai_mobile/main.dart';

void main() {
  testWidgets('ISAI App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const IsaiApp());
    expect(find.byType(IsaiApp), findsOneWidget);
  });
}
