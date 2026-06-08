import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const Dashboard = () => {
  const [energyData, setEnergyData] = useState(null);
  const [devices, setDevices] = useState([]);
  const [ecoScore, setEcoScore] = useState(78.5);
  const [carbonFootprint, setCarbonFootprint] = useState(542.4);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [dashResponse, devicesResponse, ecoResponse] = await Promise.all([
        axios.get(`${API_URL}/analytics/dashboard`),
        axios.get(`${API_URL}/devices/list`),
        axios.get(`${API_URL}/analytics/eco-score`),
      ]);
      
      setEnergyData(dashResponse.data);
      setDevices(devicesResponse.data);
      setEcoScore(ecoResponse.data.score);
      
      const carbonRes = await axios.get(`${API_URL}/analytics/carbon-footprint`);
      setCarbonFootprint(carbonRes.data.total_carbon_kg);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading ESAI Dashboard...</div>;
  }

  const consumptionData = [
    { time: '00:00', power: 1200 },
    { time: '04:00', power: 950 },
    { time: '08:00', power: 2100 },
    { time: '12:00', power: 2800 },
    { time: '16:00', power: 3200 },
    { time: '20:00', power: 2600 },
    { time: '24:00', power: 1800 },
  ];

  const deviceData = [
    { name: 'AC', value: 40 },
    { name: 'Water Heater', value: 20 },
    { name: 'Appliances', value: 20 },
    { name: 'Lighting', value: 12 },
    { name: 'Other', value: 8 },
  ];

  const COLORS = ['#ff7300', '#0088fe', '#00c49f', '#ffbb28', '#ff8042'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">🌱 ESAI Dashboard</h1>
          <p className="text-gray-600">Intelligent Sustainable Energy Management</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <p className="text-gray-600 text-sm">Current Power</p>
            <p className="text-3xl font-bold text-blue-600">{energyData?.current_consumption_w.toFixed(0) || 0}W</p>
            <p className="text-xs text-gray-500 mt-2">Real-time consumption</p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <p className="text-gray-600 text-sm">Daily Usage</p>
            <p className="text-3xl font-bold text-green-600">{energyData?.daily_consumption_kwh.toFixed(1) || 0}kWh</p>
            <p className="text-xs text-gray-500 mt-2">Today's total</p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <p className="text-gray-600 text-sm">EcoScore</p>
            <p className="text-3xl font-bold text-emerald-600">{ecoScore.toFixed(1)}/100</p>
            <p className="text-xs text-gray-500 mt-2">Sustainability rating</p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6">
            <p className="text-gray-600 text-sm">Carbon Footprint</p>
            <p className="text-3xl font-bold text-red-600">{carbonFootprint.toFixed(1)}kg</p>
            <p className="text-xs text-gray-500 mt-2">Monthly emissions</p>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Consumption Over Time */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">⚡ Power Consumption</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={consumptionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="power" stroke="#0088fe" strokeWidth={2} dot={{ fill: '#0088fe' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Energy Distribution */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Energy Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={deviceData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {deviceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Active Devices */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">🔌 Active Devices</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {devices.map((device, idx) => (
              <div key={idx} className="border border-gray-200 rounded p-4 hover:shadow-md transition">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-gray-800">{device.name}</p>
                    <p className="text-sm text-gray-600">{device.location}</p>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${
                    device.status === 'on' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {device.status.toUpperCase()}
                  </span>
                </div>
                <p className="text-lg font-bold text-blue-600 mt-2">{device.power_consumption_w.toFixed(0)}W</p>
              </div>
            ))}
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">💡 Energy Saving Recommendations</h2>
          <div className="space-y-3">
            <div className="border-l-4 border-green-500 pl-4 py-3 bg-green-50">
              <p className="font-semibold text-gray-800">Optimize AC Usage</p>
              <p className="text-sm text-gray-600">Reduce temperature by 1°C to save 2.3 kWh monthly</p>
            </div>
            <div className="border-l-4 border-blue-500 pl-4 py-3 bg-blue-50">
              <p className="font-semibold text-gray-800">Schedule Water Heater</p>
              <p className="text-sm text-gray-600">Run during off-peak hours (11 PM - 6 AM) for 15% savings</p>
            </div>
            <div className="border-l-4 border-purple-500 pl-4 py-3 bg-purple-50">
              <p className="font-semibold text-gray-800">LED Lighting Upgrade</p>
              <p className="text-sm text-gray-600">Switch remaining bulbs to LED for long-term efficiency</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;