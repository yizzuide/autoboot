# autoboot
一个Python语言的仿SpringBoot开发方式，支持IoC组件容器、注解式注册、配置驱动开发、事件通知、插件扩展的快速开发框架。
<p>
  <a href="https://pypi.org/project/autoboot">
      <img src="https://img.shields.io/pypi/v/autoboot?color=%2334D058&label=pypi%20package" alt="Version">
  </a>
  <a href="https://pypi.org/project/autoboot">
        <img src="https://img.shields.io/pypi/pyversions/autoboot.svg?color=%2334D058" alt="Python">
    </a>
    <a href="https://pepy.tech/project/autoboot">
        <img src="https://static.pepy.tech/personalized-badge/autoboot?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Downloads">
    </a>
    <a href="https://github.com/yizzuide/autoboot/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/yizzuide/autoboot" alt="License">
    </a>
</p>

## Purpose
在使用Python开发AI应用服务时遇到以下问题：

- 在`.env`里添加配置的方式，在获取配置参数时很容易写错，且调用没有代码提示。
- 配置参数较多时会让查找起来比较混乱，无法分类进行管理。
- 各种对象创建在各个函数和方法里，但多时候只需要创建一个单例。
- 很多代码和函数写在全局执行文件，创建的上下文数据在调用其它函数时需要层层传递。


## autoboot vs SpringBoot
由于Python有自身的语法特性，开发时也得到了天然的优化支持，以下是对比的测试环境：

| 开发语言 | 框架 | server |
| :----: | :----: | :----: |
| Python 3.11 | autoboot 0.7 | uvicorn
| Java 1.8 | SpringBoot 2.7 | Tomcat

- 不需要扫描组件所在的包，所有组件只需要声明即可（除Listener特殊组件需要配置扫描外）。
- 所有声明的组件只有在调用时才会创建并缓存，实现了SpringBoot推荐的懒加载创建方式。
- 配置采用`.env + yaml`组合，`.env`用于支持多环境配置项，主配置仅为`autoboot.yaml`，框架扩展了自定义指令`!env`用于从`.env`取值。
- 微服务项目的启动速度快到可以在1-2秒内启动完成，相比SpringBoot的10几秒，快了至少10倍。

## Quick Start

### Install
```bash
pip install autoboot
```

### Usage

#### 配置
* 启动配置文件：./config/.env

```ini
# 配置环境
ENV_NAME=dev

# 应用名
APPLICATION_NAME=demo
```

* 环境配置文件：./config/.env.dev

```ini
APPLICATION_NAME=demo-dev
```

* 主配置文件：./config/autoboot.yaml

```yml
autoboot:
  application:
    # !env 引用 .env 里的配置参数 
    name: !env APPLICATION_NAME
    # 微服务模块名
    module: api
    # 日志
    log:
      dir: logs
      # !!str 明确定义为字符串类型
      max_size: !!str 100 MB
      retention: !!str 30 days
```

#### 创建并启动容器上下文
```python
from autoboot import AutoBoot, AutoBootConfig

context = Autoboot(AutoBootConfig(config_dir="./config"))
context.run()

# 或者直接使用 loguru.logger，日志的配置同样生效
Autoboot.logger.info("Context run succeed!")
```

## Advanced Features

### 自定义配置

#### 在主配置里添加
```yml
api:
  # 在环境配置文件.env添加：API_SECRET_KEY=xxx
  secret: !env API_SECRET_KEY
```

#### 创建配置类: api_properties.py
```python
from autoboot.annotation.env import value_component

class ApiProperties:

  @value_component("api.secret")
  @staticmethod
  def secret() -> str:
    # 返回的值作为默认的配置值
    return ""
```

#### 导入并使用配置
```python
from autoboot import AutoBoot, AutoBootConfig
from .api_properties import ApiProperties

context = Autoboot(AutoBootConfig(config_dir="./config"))
context.run()

# 在容器启动完成后获取
Autoboot.logger.info("api.secret: {}", ApiProperties.secret())
```

### 监听容器事件

#### 主配置文件
```yml
autoboot:
  application:
    # 扫描监听器包
    scan_listener_packages:
      - listener
```      

#### 项目下创建目录`listener`

在该目录创建`__init__.py`，添加以下内容：

```python
from .app_listener import AppListener

__all__ = ["MyListener"]
```

在该目录创建`app_listener.py`，添加以下内容：

```python
from autoboot import AutoBoot
from autoboot.event import ApplicationListener
from autoboot.meta import Listener

@Listener
class AppListener(ApplicationListener):

  def on_env_prepared(self, config: dict[str, Any]):
    AutoBoot.logger.info("listen: env prepared!")
  
  def on_started(self):
    AutoBoot.logger.info("listen: app started!")

```

### 发送事件

#### 基于Action的事件发送与监听
```python
from dataclasses import dataclass
from autoboot.event import emitter, Event
from loguru import logger

@dataclass
class PayOrder:
  no: str

@emitter.on("pay_action")
def received_payment(event: Event[str]):
  logger.info("received_payment")
  assert(event.data == "pay order: 1001")


emitter.emit(action="pay_action", event=Event("pay order: 1001"))
```

#### 基于事件类型自动匹配的发送与监听
```python
from dataclasses import dataclass
from autoboot.event import emitter, Event
from loguru import logger

@dataclass
class PayOrder:
  no: str

@emitter.on_event
def received_pay(event: Event[PayOrder]):
  logger.info("received_pay")
  assert(event.data == PayOrder("1001"))

emitter.emit(event=Event(PayOrder("1001")))
```

### 扩展插件
#### 创建插件: my_plugin.py
```python
from autoboot.plugin import AppPlugin

class MyPlugin(AppPlugin):
  def install(self):
    AutoBoot.logger.info("plugin: installed!")

  def on_env_prepared(self, config: dict[str, Any]):
    AutoBoot.logger.info("plugin: env prepared!")

  def on_started(self):
    AutoBoot.logger.info("plugin: started!")
```

#### 安装插件
```python
from autoboot import AutoBoot, AutoBootConfig
from .my_plugin import MyPlugin

context = Autoboot(AutoBootConfig(config_dir="./config"))
context.apply(MyPlugin())
context.run()
```

#### 注册插件
```python
from autoboot.plugin import PluginManager

PluginManager.register(MyPlugin)
```

### 扩展事件
#### 创建事件
```python
from autoboot.event import Event

class PayOrder(Event):
  pass
```

#### 注册事件
```python
from autoboot.event import EventManager

## Contributors
有问题可以在issues开话题讨论，如果你有新的想法，创建新的`feat`或`pref`分支并提交PR。

## License
[MIT License](https://github.com/yizzuide/autoboot/blob/main/LICENSE)
