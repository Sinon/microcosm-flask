template = """
    <!doctype html>
    <html class="no-js" lang="">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="x-ua-compatible" content="ie=edge">
            <title>{{ service_name | capitalize }}</title>
            <meta name="description" content="Landing">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet">
        </head>
        <style>
            html {
                font-family: sans-serif;
                -ms-text-size-adjust: 100%;
                -webkit-text-size-adjust: 100%;
                font-size: 10px;
                -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
            }
            body {
                margin: 0;
                font-family: "Open Sans", sans-serif;
                font-size: 14px;
                line-height: 1.42857143;
                color: #333333;
                background-color: #fff;
            }
            a {
                background-color: transparent;
                color: #337ab7;
                text-decoration: none;
            }

            h1 {
                font-weight: 500;
                line-height: 1.1;
                color: inherit;
                padding-top: 2%;
                text-transform: capitalize;
            }
            pre {
                background-color: #E8E8E8;
                border-style: solid;
                border-width: 1px;
            }
            .section {
                margin: 0 100px;
            }
            .text-center {
                text-align: center;
            }
            #env-button {
                float: right;
                margin: 5px;
            }
        </style>
        <body>
            <h1 class="text-center">{{ service_name }}</h1>
            {%- if description -%}
            <h3 class="text-center">{{ description }}</h2>
            {%- endif -%}
            <h3 class="text-center">{{ version }}</h3>
            <div class="section">
                <h2><a href="api/health">Health</a></h2>
                <pre id=health>{{ health }}</pre>
            </div>
            {%- for swagger_version in swagger_versions -%}
                <div class="section">
                    <h2><a href="api/{{ swagger_version }}/swagger">Swagger ({{ swagger_version }})</a></h2>
                </div>
            {%- endfor -%}
            {%- if homepage -%}
                <div class="section">
                    <h2><a href={{ homepage }}>Home Page</a></h2>
                </div>
            {%- endif -%}
            <div class="section">
                <h2><a href="api/config">Config</a></h2>
                <div>
                    <a id="env-button" href="data:text/plain;charset=utf-8,
                    {%- for item in env | sort -%}
                        {{ item | urlencode }}%0A
                    {%- endfor %}" download="{{ service_name }}_env"><button>Download Env</button></a>
                    <pre id=config>{{ config }}</pre>
                </div>
            </div>
            {%- if links -%}
            <div class="section">
                <h2>Links</h2>
                {%- for link in links -%}
                <ul>
                    <li>
                        <a href="{{ links[link] }}">{{ link | replace("_", " ") | capitalize }}</a>
                    </li>
                </ul>
                {%- endfor -%}
            </div>
            {%- endif -%}
        </body>
    </html>
"""
