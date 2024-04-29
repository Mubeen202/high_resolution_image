import React, { useState } from 'react';
import ImageUploader from './Components/ImageUploader';
import FilteredImage from './Components/FilteredImage';
import DemoImages from './Components/DemoImages';

function App() {
  const [filteredImageUrl, setFilteredImageUrl] = useState(null);

  const handleImageUpload = (image) => {
    // Call your backend API to process the image here
    // Replace with your actual API call and logic
    setFilteredImageUrl('placeholder-filtered-image.jpg');  // Simulate filtered image for now
  };

  const handleDemoImageClick = (demoImageName) => {
    // Handle demo image selection (optional)
    // You can display a placeholder filtered image and disable download
    setFilteredImageUrl('placeholder-filtered-image.jpg');
  };

  const handleDownload = () => {
    // Implement download functionality here (consider browser compatibility)
    // You can right-click download or create a download link
  };

  return (
    <div className="container">
      <p>Hellow World</p>
      {/* <ImageUploader onImageUpload={handleImageUpload} />
      <FilteredImage imageUrl={filteredImageUrl} onDownload={handleDownload} />
      <DemoImages onDemoImageClick={handleDemoImageClick} /> */}
    </div>
  );
}

export default App;
