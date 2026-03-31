
export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <h1 className="text-4xl font-bold text-primary-600 mb-4">Dealix - ديليكس</h1>
      <p className="text-xl text-gray-600 mb-8">منصة إدارة الصفقات والتسويق بالعمولة الذكية</p>
      <a href="/dashboard" className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium">دخول لوحة التحكم</a>
    </div>
  );
}
