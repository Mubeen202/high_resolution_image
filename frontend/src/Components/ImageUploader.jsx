import React, { useState } from 'react';

const ImageUploader = ({ onImageUpload }) => {
  const [imageFile, setImageFile] = useState(null);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImageFile(file);
      onImageUpload(file);  // Call callback function with uploaded image
    }
  };

  return (
    <div className="image-section">
      <h2>Before</h2>
      <img id="before-image" src={imageFile ? URL.createObjectURL(imageFile) : ''} alt="" />
      <input type="file" accept="image/*" onChange={handleUpload} />
    </div>
  );
};

export default ImageUploader;
