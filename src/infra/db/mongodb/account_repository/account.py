from src.data.protocols.add_account_repository import AddAccountRepository
from src.domain.models.account import AccountModel
from src.domain.usecases.add_account import AddAccountModel
from src.infra.db.mongodb.helpers.mongo_helper import MongoHelper


class AccountMongoRepository(AddAccountRepository):
    mongo_helper: MongoHelper = MongoHelper()

    async def add(self, account_data: AddAccountModel) -> AccountModel:
        account_collection = self.mongo_helper.get_collection('account')
        document = await account_collection.insert_one(account_data.model_dump())
        document = await account_collection.find_one({"_id": document.inserted_id})
        self.mongo_helper.disconnect()
        return AccountModel(**self.mongo_helper.mapper(document))
