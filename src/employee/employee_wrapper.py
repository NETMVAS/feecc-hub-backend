from loguru import logger

from src.database.database import base_mongodb_wrapper
from src.feecc_workbench.utils import time_execution
from src.feecc_workbench.exceptions import EmployeeNotFoundError
from src.feecc_workbench.Types import Document
from .Employee import Employee


class EmployeeWrapper:
    collection = "employeeData"

    @time_execution
    def get_employee_by_card_id(self, card_id: str) -> Employee:
        """find the employee with the provided RFID card id"""
        filters = {"rfid_card_id": card_id}
        projection = {"_id": 0}
        employee_data: list[Document] | None = base_mongodb_wrapper.read(collection=self.collection, filters=filters, projection=projection)

        if employee_data is None:
            message = f"No employee with card ID {card_id}"
            logger.error(message)
            raise EmployeeNotFoundError(message)

        return Employee(**employee_data[0])


employee_wrapper = EmployeeWrapper()
