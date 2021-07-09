import React, { ReactElement } from 'react';
//import Modal from "react-modal";
//import styled, { keyframes } from "styled-components";
import "./Modal.css";

//Modal.setAppElement("#root");


const Modal = (props) => {
    const { open, close } = props;

    return (
        <div className={ open ? 'openModal modal':'modal'}>
            { open ? (
                <section>
                    <header>
                        <h3>이미지 등록하기</h3>
                        <button className="close" onClick={close}>&times;</button>
                    </header>
                    <main>
                        {props.children}
                    </main>
                    <footer>
                        <button className="close" onClick={close}>
                            close
                        </button>
                    </footer>                       
                </section>
            ): null} 
        </div>
    );
}
export default Modal