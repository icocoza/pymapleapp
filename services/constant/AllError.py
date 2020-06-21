from enum import Enum, auto

class AllError(Enum):

	ok = auto()
	NoServiceCode = auto()
	NotAvailableServiceCode = auto()
	NotImplemented = auto()
	invalid_command = auto()
	failed_search = auto()
	invalid_search = auto()
	empty_search = auto()
	no_search_result = auto()
	
	invalid_from_addressid = auto()
	invalid_to_addressid = auto()
	
	empty_goods_name = auto()
	empty_goods_size = auto()
	empty_goods_weight = auto()
	empty_goods_type = auto()
	empty_goods_price = auto()
	empty_order_begintime = auto()
	empty_order_endtime = auto()
	empty_gpslist = auto()
	failed_to_saveorder = auto()
	
	invalid_offset_count = auto()
	empty_order_list = auto()
	no_order_data = auto()
	
	not_exist_order = auto()
	late_delivery_request = auto()
	already_assigned_order = auto()
	failed_assign_deliver = auto()
	not_authorized_user = auto()
	not_assigned_order = auto()
	not_start_order = auto()
	not_allowed_order = auto()
	not_started_order = auto()
	not_receipt_order = auto()
	not_delivering_order = auto()
	not_arrived_order = auto()
	not_delivered_order = auto()
	already_starting_order = auto()
	failed_cancel_delivery_ready = auto()
	already_occupied_order = auto()
	failed_apply_order = auto()
	failed_to_saveassign = auto()
	failed_to_savestartmoving = auto()
	failed_to_savebeforegotcha = auto()
	failed_to_savegotcha = auto()
	failed_to_savedelivering = auto()
	failed_to_savebeforedelivered = auto()
	failed_to_savedelivered = auto()
	failed_to_saveconfirm = auto()
	failed_to_cancelbysender = auto()
	failed_to_cancelbydeliver = auto()
	failed_to_updateordercancel = auto()
	impossible_cancel_delivery = auto()
	invalid_start_passcode = auto()
	invalid_end_passcode = auto()
	no_permission = auto()
	not_exist_deliver = auto()
	InvalidEmailFormat = auto()

	ShortPasswordLengthThan8 = auto()
	RegisterFailed = auto()

	AlreadyExistScode = auto()
	NotExistScode = auto()
	ScodeAllowedOnlyAlphabet = auto()
	FailedToCreateDatabase = auto()
	InvalidDbParameter = auto()
	failedToCreateApp = auto()

	WrongAccountInfo = auto()
	
	FailedToUpdateApp = auto()
	
	NotExistUser = auto()
	
	mismatch_token_or_expired_token = auto()
	
	wrong_appid = auto()
	unknown_datatype = auto()
	
	UnknownAuthType = auto()
	FailedUserRegister = auto()
	ExistUserName = auto()
	NotExistUserId = auto()
	ExistPhoneNo = auto()
	ExistEmail = auto()
	appTokenNotExist = auto()
	appTokenNotValidated = auto()
	
	userIdMoreThan6Characters = auto()
	userid_alphabet_and_digit = auto()
	passwordMoreThan8Characters = auto()
	EmptyOldPassword = auto()

	InvalidMobileFormat = auto()
	smscode_size_4 = auto()
	mismatch_smscode = auto()
	
	invalid_app_token = auto()
	invalid_user_token = auto()
	ExpiredOrDifferentLoginToken = auto()
	ExpiredLoginToken = auto()
	ExpiredSigninToken = auto()
	InvalidUUID = auto()
	unauthorized_token = auto()
	InvalidAdminToken = auto()
	InvalidLoginToken = auto()
	InvalidSigninToken = auto()
	MightBeLeftUser = auto()

	mismatch_token = auto()
	NotExistUserAuth = auto()
	not_exist_userinfo = auto()
	not_exist_building = auto()

	ExpiredAdminToken = auto()
	invalid_or_expired_token = auto()
	UnauthorizedUserId = auto()
	UnauthorizedAnonymousUserId = auto()
	InvalidUser = auto()
	failed_email_verify = auto()
	failed_phone_Verify = auto()
	FailToChangePW = auto()
	FailedUpdateToken = auto()
	MismatchOldPassword = auto()
	SameWithOldPassword = auto()
	WrongPassword = auto()
	
	eNotExistIds = auto()
	FailToCreateAnonymousAccount = auto()
	NoSession = auto()
	FailAddBoard = auto()
	FailDeleteBoard = auto()
	FailUpdate = auto()
	FailAddReply = auto()
	FailDeleteReply = auto()
	FailAddVoteUser = auto()
	FailDelVoteUser = auto()
	NotExistLikedUser = auto()
	NotExistDislikeUser = auto()
	NotExistVoteUser = auto()
	NotExistVoteInfo = auto()
	AlreadyLiked = auto()
	AlreadyDisliked = auto()
	AlreadyVoteUser = auto()
	AlreadyExpired = auto()
	NoData = auto()
	NoListData = auto()
	InvalidParameter = auto()
	InvalidCategoryId = auto()
	PermissionDeny = auto()
	WrongAptCode = auto()
	VoteItemHas2More = auto()
	
	NoChannel = auto()
	FailToUpdate = auto()

	complete = auto()
	exception = auto()
	commit_error = auto()
	invalid_file_session = auto()
	invalid_file_size = auto()
	invalid_file_name = auto()
	invalid_fileid = auto()
	too_large_file = auto()
	too_small_file = auto()
	fail_to_uploadfile = auto()
	fail_to_loadfile = auto()
	fail_to_createfile = auto()
	not_exist_fileinfo = auto()
	
	invalid_orderid = auto()
	mismatch_orderid_deliverid = auto()

	NoMessage = auto()
	AlreadyReadMessage = auto()
	FailToSaveMessage = auto()
	FailToDeleteMessage = auto()
	FailToUpdateChannel = auto()

	eNoServiceCommand = auto()

	UnauthorizedUser = auto()
	UnauthorizedOrExpiredUser = auto()
	FailToMakePooling = auto()
	unknown_error = auto()