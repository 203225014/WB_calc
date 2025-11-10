// frontend/src/pages/Calculator.js
import React, { useState } from 'react';

const calcLogistics = (volume, coeff) => {
  if (volume >= 1) {
    const roundedVolume = Math.ceil(volume);
    const base = 0.46 * coeff;
    const additional = (roundedVolume - 1) * (0.14 * coeff);
    return base + additional;
  } else if (volume > 0.8) return 0.32 * coeff;
  else if (volume > 0.6) return 0.30 * coeff;
  else if (volume > 0.4) return 0.29 * coeff;
  else if (volume > 0.2) return 0.26 * coeff;
  else if (volume >= 0.001) return 0.23 * coeff;
  else return 0;
};

const format = (n) => (isFinite(n) ? n.toFixed(2) : "—");

const Calculator = () => {
  const [inputs, setInputs] = useState({
    purchase: 835,
    profit: 230,
    len: 30,
    wid: 28,
    hei: 9,
    commission: 25,
    acquiring: 3,
    tax: 8,
    adsPct: 10,
    logiCoeff: 400,
    returnCost: 50,
    buyout: 90,
    storage: 12,
  });

  const [results, setResults] = useState({
    volume: "—",
    logistics: "—",
    logisticsTotal: "—",
    clientPrice: "—",
    adsVal: "—",
    commissionVal: "—",
    acquiringVal: "—",
    taxVal: "—",
    storageVal: "—",
    finalCost: "—",
    profitVal: "—",
    margin: "—",
  });

  const [adsWarning, setAdsWarning] = useState("");

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    const numericValue = Number(value);
    setInputs((prev) => ({
      ...prev,
      [name]: isNaN(numericValue) ? 0 : numericValue,
    }));
    e.target.value = isNaN(numericValue) ? "0" : String(numericValue);
  };

  const performCalculation = () => {
    const { purchase, profit, len, wid, hei, commission, acquiring, tax, logiCoeff, returnCost, buyout, storage } = inputs;
    let { adsPct } = inputs;

    let warningText = "";
    if (adsPct > 59.99) {
      adsPct = 59.99;
      warningText = "⚠️ Фига ты Маркетолог! Пересчитай рекламу)))";
    }
    setAdsWarning(warningText);

    const volumeLiters = (len * wid * hei) / 1000;
    const logistics = calcLogistics(volumeLiters, logiCoeff);
    const logisticsTotal = (logistics + (1 - buyout / 100) * returnCost) / (buyout / 100);
    const baseCost = purchase + logisticsTotal + storage;

    const p = (commission + acquiring + tax) / 100;
    const k = adsPct / 100;
    const totalPerc = p + k;
    if (1 - totalPerc <= 0) {
      setResults((prev) => ({
        ...prev,
        clientPrice: "Ошибка: проценты >= 100%",
        volume: format(volumeLiters),
        logistics: format(logistics),
        logisticsTotal: format(logisticsTotal),
      }));
      return;
    }

    const clientPrice = (baseCost + profit) / (1 - totalPerc);
    const adsRub = clientPrice * k;
    const commRub = (clientPrice * commission) / 100;
    const acqRub = (clientPrice * acquiring) / 100;
    const taxRub = (clientPrice * tax) / 100;
    const finalCost = baseCost + commRub + acqRub + taxRub + adsRub;
    const pureProfit = clientPrice - finalCost;
    const marginPct = (pureProfit / clientPrice) * 100;

    setResults({
      volume: format(volumeLiters),
      logistics: format(logistics),
      logisticsTotal: format(logisticsTotal),
      clientPrice: format(clientPrice),
      adsVal: format(adsRub),
      commissionVal: format(commRub),
      acquiringVal: format(acqRub),
      taxVal: format(taxRub),
      storageVal: format(storage),
      finalCost: format(finalCost),
      profitVal: format(pureProfit),
      margin: format(marginPct),
    });
  };

  const handleCalculateClick = (e) => {
    e.preventDefault();
    performCalculation();
  };

  const handleResetClick = () => {
    setInputs({
      purchase: 0,
      profit: 0,
      len: 0,
      wid: 0,
      hei: 0,
      commission: 0,
      acquiring: 0,
      tax: 0,
      adsPct: 0,
      logiCoeff: 0,
      returnCost: 0,
      buyout: 0,
      storage: 0,
    });
    setResults({
      volume: "—",
      logistics: "—",
      logisticsTotal: "—",
      clientPrice: "—",
      adsVal: "—",
      commissionVal: "—",
      acquiringVal: "—",
      taxVal: "—",
      storageVal: "—",
      finalCost: "—",
      profitVal: "—",
      margin: "—",
    });
    setAdsWarning("");
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold text-center mb-6 text-wb-accent-alt">
        Калькулятор юнит-экономики
      </h2>

      <div className="flex flex-col md:flex-row gap-6">
        {/* Ввод данных */}
        <div className="bg-wb-box p-6 rounded-xl shadow-lg w-full md:w-1/2">
          <h3 className="text-xl mb-4 text-wb-accent-alt">Ввод данных</h3>

          {/* === ВСЕ ПОЛЯ ВВОДА === */}
          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <div className="flex-1">
              <label className="block text-sm text-gray-400 mb-1">Цена закупки (₽)</label>
              <input type="number" name="purchase" value={inputs.purchase} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" />
            </div>
            <div className="flex-1">
              <label className="block text-sm text-gray-400 mb-1">Желаемая прибыль (₽)</label>
              <input type="number" name="profit" value={inputs.profit} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" />
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Длина (см)</label>
              <input type="number" name="len" value={inputs.len} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Ширина (см)</label>
              <input type="number" name="wid" value={inputs.wid} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Высота (см)</label>
              <input type="number" name="hei" value={inputs.hei} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Комиссия WB (%)</label>
              <input type="number" name="commission" value={inputs.commission} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Эквайринг (%)</label>
              <input type="number" name="acquiring" value={inputs.acquiring} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Налог (%)</label>
              <input type="number" name="tax" value={inputs.tax} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <div className="flex-1">
              <label className="block text-sm text-gray-400 mb-1">Реклама (% от цены)</label>
              <input type="number" name="adsPct" value={inputs.adsPct} onChange={handleInputChange}
                className={`w-full p-2 rounded-lg bg-wb-input border ${inputs.adsPct > 59.99 ? 'border-red-500 ring-2 ring-red-500' : 'border-gray-700'} text-white`} />
              {adsWarning && (<div className="mt-1 text-sm text-red-500 animate-pulse">{adsWarning}</div>)}
            </div>
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Стоимость логистики (коэф.)</label>
              <input type="number" name="logiCoeff" value={inputs.logiCoeff} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Стоимость возврата (₽)</label>
              <input type="number" name="returnCost" value={inputs.returnCost} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Процент выкупа (%)</label>
              <input type="number" name="buyout" value={inputs.buyout} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
            <div className="flex-1"><label className="block text-sm text-gray-400 mb-1">Хранение (₽)</label>
              <input type="number" name="storage" value={inputs.storage} onChange={handleInputChange}
                className="w-full p-2 rounded-lg bg-wb-input border border-gray-700 text-white" /></div>
          </div>

          <div className="flex gap-4">
            <button onClick={handleCalculateClick}
              className="flex-1 px-4 py-2 bg-wb-accent text-white font-semibold rounded-lg shadow-md hover:bg-[#8a3fd9] transition">
              Рассчитать
            </button>
            <button onClick={handleResetClick}
              className="flex-1 px-4 py-2 bg-red-600 text-white font-semibold rounded-lg shadow-md hover:bg-red-700 transition">
              Сбросить
            </button>
          </div>
        </div>

        {/* Результаты */}
        <div className="bg-wb-box p-6 rounded-xl shadow-lg w-full md:w-1/2">
          <h3 className="text-xl mb-4 text-wb-accent-alt">Результаты</h3>

          {/* --- Главные результаты --- */}
          <div className="mb-4 p-4 rounded-lg bg-[#1f1f27] border border-wb-accent/40 shadow-inner text-center">
            <div className="mb-2">
              <span className="block text-sm text-gray-400">Цена клиента, ₽</span>
              <span className="text-3xl font-bold text-wb-accent-alt">{results.clientPrice}</span>
            </div>
            <div>
              <span className="block text-sm text-gray-400">Прибыль (на ед.), ₽</span>
              <span className="text-2xl font-bold text-green-400">{results.profitVal}</span>
            </div>
          </div>

          {/* --- Остальные результаты --- */}
          <div className="space-y-2">
            {[
              ['Объём (л):', results.volume],
              ['Логистика, ₽:', results.logistics],
              ['Логистика итого, ₽:', results.logisticsTotal],
              ['Реклама, ₽:', results.adsVal],
              ['Комиссия WB, ₽:', results.commissionVal],
              ['Эквайринг, ₽:', results.acquiringVal],
              ['Налог, ₽:', results.taxVal],
              ['Хранение, ₽:', results.storageVal],
              ['Финальная себестоимость, ₽:', results.finalCost],
              ['Маржинальность, %:', results.margin],
            ].map(([label, value]) => (
              <div key={label} className="flex justify-between border-b border-gray-700 pb-1">
                <span>{label}</span>
                <span className="text-wb-accent-alt font-medium">{value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Calculator;
