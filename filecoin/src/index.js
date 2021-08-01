import * as React from "react";
import {css} from "@emotion/react";

const API_KEY = "SLA74d74d8e-1eb5-42c6-968b-a121644f5064TE";

STYLES_PAGES = css "
    margin: 0;
    padding: 0;
";

export default class Testpage extends React.Component {
    _handleUpload = (e) => {

    }
    render() {
        return <div>Hey
        <input type='file' onChange = {this._handleUpload} />
        </div>;
    }
}