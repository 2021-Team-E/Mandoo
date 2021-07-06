import React from 'react';
import BlankTop from '../components/BlankTop';
import {useHistory} from 'react-router-dom';
import {useState} from 'react';

const border = {
    marginTop: "40px",
    marginBottom: "40px",
    border: "1px solid black",
    width: "150px",
    height: "200px"
};

const MainPage = () => {
    
    const history = useHistory();
    const [fileUrl, setFileUrl] = useState(null);

    function processImage(event) {
        const imageFile = event.target.files[0];
        const imageUrl = URL.createObjectURL(imageFile);
        setFileUrl(imageUrl)
    }
 
    return(
        <div>
            
            <BlankTop DesktopMargin='3' TabletMargin='3' MobileMargin='1'/>
            <button onClick={() => history.push((`/`))}>메인페이지</button>
            <button onClick={() => history.push((`/signup`))}>회원가입</button>
            <button onClick={() => history.push((`/login`))}>로그인</button>
            <div style={border}>
                 <img style={{"object-fit": "fill", "width": "150px", "height": "200px"}} src={fileUrl} alt={fileUrl} />
            </div>
            <div>
                <input type='file'
                    accept='image/*'
                    name='question_img'
                    onChange={processImage}>
                </input>
            </div>
        </div>
    );
}



export default MainPage