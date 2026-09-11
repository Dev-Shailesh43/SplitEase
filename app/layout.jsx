import './globals.css';

export const metadata = {
  title: 'SplitEase 2.0 - Premium Campus P2P Settlements',
  description: 'A modern, dynamic fintech app for campus expense tracking and smart debt settlement.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
