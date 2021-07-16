import React from 'react';
import ReactLoading from 'react-loading';

function Loader({ type, color, message }) {
  return (
    <div class="contentWrap">
      <div
        style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          marginLeft: 'auto',
          marginRight: 'auto',
        }}
      >
        <h2>{message}</h2>
        <h2>창을 닫지 마세요.</h2>
        <ReactLoading type={type} color={color} height={'80%'} width={'80%'} />
      </div>
    </div>
  );
}

export default Loader;
