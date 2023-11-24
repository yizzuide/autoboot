from result import Ok, Err
from loguru import logger
from autoboot.annotation.effect import retry

def test_retry():
  
  @retry(tries=3, delay=1)
  def request():
    # test throw exception
    # 1 / 0
    pass
    

  match request():
    case Ok(value):
      logger.info(f"val = {value}")
    case Err(value):
      logger.error(f"err = {value}")