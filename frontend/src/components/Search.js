import React from 'react';

function Search({ onSubmit }) {
  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(event.target.elements.filter.value);
  };

  return (
    <form onSubmit={handleSubmit} align="left">
      <input style={{ marginLeft: '5px' }} name="filter" />
      <button style={{ color: '#369', margin: '5px', backgroundColor: 'white' }}>Search</button>
    </form>
  );
}

export default Search;
