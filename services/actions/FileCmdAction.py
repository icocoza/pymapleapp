import os, sys, json, datetime
from services.constant.MapleCmd import MapleCmd
from common.utils.StrUtils import StrUtils
from services.constant.AllError import AllError
from services.actions.Action import Action

from repository.db.file.FileRepository import FileRepository
import common.config.appconfig as appconfig

class FileCmdAction:
    def __init__(self):
        super().__init__()

        self.fileRepository = FileRepository()
        
    def uploadFile(self, scode, session, jdata):
        pass

    def __uploadFile(self, ):
        fileId = StrUtils.getSha256Uuid('fileId:')

#     def download(self, scode, userId, url, savePath):
#         if url is None:
#             return None, None
#         filename = (str(int(datetime.now().microsecond / 1000)))+'-'+ url.split('/')[-1]
#         path = os.path.join(savePath, scode, userId)
#         if os.path.exists(path) == False:
#             os.makedirs(path)
#         savePath = os.path.join(path, filename)

#         r = requests.get(url, allow_redirects=True)
#         open(savePath, 'wb').write(r.content)

#         return savePath, os.stat(savePath).st_size
 


#     private String uploadFile(MultipartFile file, String scode, String userName, String uploadDir, String serverIp, String comment) {
#         String fileId = StrUtils.getUuid("file");
#         Path savePath = Paths.get(uploadDir, scode, fileId);

#         try {
#             file.transferTo(savePath);
#         } catch (IOException e) {
#             return null;
#         }

#         List<String> queries = new ArrayList<>();

#         String userId = userCommonRepository.findUserIdByUserName(scode, userName);
#         Long fileSize = file.getSize();
#         EUploadFileType eType = EUploadFileType.getType(FileUtils.getFileExt(file.getOriginalFilename()));;
#         queries.add(fileCommonRepository.queryInitFileInfo(scode, fileId, userId, serverIp, userName, eType.getValue(), fileSize, comment));

#         ImageUtil.ImageSize imageSize = null;
#         try {
#             imageSize = ImageUtil.getImageSize(new File(savePath.getFileName().toString()));
#         } catch (IOException e) {
#             return null;
#         }
#         queries.add(fileCommonRepository.queryUpdateFileInfo(scode, fileId, imageSize.getWidth(), imageSize.getWidth(), fileSize));


#         float rate = imageSize.getWidth() > imageSize.getHeight()? FileConfig.THUMB_SIZE / (float)imageSize.getWidth() : FileConfig.THUMB_SIZE / (float)imageSize.getHeight();
#         String thumbName = newThumbFilename();
#         int thumbWidth = (int)(imageSize.getWidth() * rate);
#         int thumbHeight = (int)(imageSize.getHeight() * rate);
#         String thumbFilePath = getThumbPath(scode, thumbName);

#         imageResizeWorker.doResize(savePath.toString(), thumbFilePath, thumbWidth, thumbHeight, new ImageResizeWorker.ImageResizerCallback() {
#             @Override
#             public void onCompleted(Object dest) {
#                 log.error("Completed - " + dest);
#             }

#             @Override
#             public void onFailed(Object src) {
#                 log.error("Failed - " + src);
#             }
#         });
#         queries.add(fileCommonRepository.queryUpdateThumbnail(scode, fileId, thumbName, thumbWidth, thumbHeight));
#         fileCommonRepository.multiQueries(scode, queries);
#         return fileId;
#     }

#     private static int seq = 0;
#     private String newThumbFilename() {
#         return String.format("%s%d_%03d", FileConfig.THUMB_PATH, System.currentTimeMillis(), ++seq % 1000);
#     }

#     private String getThumbPath(String scode, String fileName) {
#         return Paths.get(FileConfig.UPLOADED_FOLDER, scode, FileConfig.THUMB_PATH, fileName).toString();
#     }


#   ICommandFunction<AuthSession, ResponseData<EAllError>, FileForm.UploadForm> doUploadFile = (AuthSession authSession, ResponseData<EAllError> res, FileForm.UploadForm form) -> {
#         List<FileResult> fileIds = new ArrayList<>();
#         String fileId = uploadFile(form.getMultipartFile(), form.getScode(), form.getUserName(), form.getUploadDir(), form.getServerIp(), form.getComment());
#         fileIds.add(new FileForm().new FileResult(form.getMultipartFile().getOriginalFilename(), fileId));
#         res.setParam("fileIds", fileIds);
#         return res.setError(EAllError.ok);
#     };

#     ICommandFunction<AuthSession, ResponseData<EAllError>, FileForm.MultiUploadForm> doMultiUploadFile = (AuthSession authSession, ResponseData<EAllError> res, FileForm.MultiUploadForm form) -> {
#         List<MultipartFile> files = form.getMultipartFiles();
#         List<FileResult> fileIds = new ArrayList<>();
#         for(MultipartFile file : files) {
#             String fileId = uploadFile(file, form.getScode(), form.getUserName(), form.getUploadDir(), form.getServerIp(), form.getComment());
#             fileIds.add(new FileForm().new FileResult(file.getOriginalFilename(), fileId));
#         }
#         res.setParam("fileIds", fileIds);
#         return res.setError(EAllError.ok);
#     };