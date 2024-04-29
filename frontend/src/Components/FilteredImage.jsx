import React, { useState } from 'react';
import ImageUploader from './ImageUploader';
import FilteredImage from './FilteredImage';
import DemoImages from './DemoImages';

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
      <ImageUploader onImageUpload={handleImageUpload} />
      <FilteredImage imageUrl={filteredImageUrl} onDownload={handleDownload} />
      <DemoImages onDemoImageClick={handleDemoImageClick} />
    </div>
  );
}

export default App;
