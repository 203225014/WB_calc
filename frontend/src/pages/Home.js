// frontend/src/pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-4">
      <h1 className="text-4xl md:text-5xl font-bold text-center mb-6 text-wb-accent">
        Юнит-калькулятор Wildberries
      </h1>
      <p className="text-lg text-center mb-8 text-wb-light max-w-2xl">
        Рассчитайте юнит-экономику ваших товаров на маркетплейсе Wildberries быстро и удобно.
      </p>
      <Link
        to="/calculator"
        className="px-6 py-3 bg-wb-accent text-white font-semibold rounded-lg shadow-md hover:bg-[#8a3fd9] focus:outline-none focus:ring-2 focus:ring-wb-accent focus:ring-opacity-50 transition duration-300"
      >
        Начать расчёт
      </Link>
    </div>
  );
};

export default Home;