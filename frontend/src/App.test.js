import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the home headline', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /tenue à jour par l'IA/i })).toBeInTheDocument();
});
