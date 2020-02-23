import gaussian_pyramid


class LucasKanade:

    def __init__():
   
    def get_fx(src1, src2) : 
        fx = np.arrays(src1.size())
        kernel = np.zeros((2,2))
        kernel[0][0] = -1.0
        kernel[1][0] = -1.0

        filter2D(src1, dst1, -1, kernel)
        filter2D(src2, dst2, -1, kernel)

        fx = dst1 + dst2

        return fx

    def get_fy(src1, src2) : 
        fy = np.arrays(src1.size())
        kernel = np.zeros((2,2))
        kernel[0][0] = -1.0
        kernel[0][1] = -1.0

        filter2D(src1, dst1, -1, kernel)
        filter2D(src2, dst2, -1, kernel)

        fy = dst1 + dst2

        return fy
    


    def getLucasKanadeOpticalFlow(self, frame1, frame2, flow_u, flow_v):

    




    def EndPointError(output, gt):

        if output.size(1) == 1:  # stereo
           output = disp2flow(output)
        output = resize_dense_vector(output, gt.size(2), gt.size(3))
        error = torch.norm(output - gt[:, :2, :, :], 2, 1, keepdim=False)
        if gt.size(1) == 3:
           mask = (gt[:, 2, :, :] > 0).float()
        else:
           mask = torch.ones_like(error)
        epe = (error * mask).sum() / mask.sum()
        
        return epe.reshape(1)









Mat get_fx(Mat &src1, Mat &src2){
    Mat fx;
    Mat kernel = Mat::ones(2, 2, CV_64FC1);
    kernel.ATD(0, 0) = -1.0;
    kernel.ATD(1, 0) = -1.0;

    Mat dst1, dst2;
    filter2D(src1, dst1, -1, kernel);
    filter2D(src2, dst2, -1, kernel);

    fx = dst1 + dst2;
    return fx;
}

Mat get_fy(Mat &src1, Mat &src2){
    Mat fy;
    Mat kernel = Mat::ones(2, 2, CV_64FC1);
    kernel.ATD(0, 0) = -1.0;
    kernel.ATD(0, 1) = -1.0;

    Mat dst1, dst2;
    filter2D(src1, dst1, -1, kernel);
    filter2D(src2, dst2, -1, kernel);

    fy = dst1 + dst2;
    return fy;
}

Mat get_ft(Mat &src1, Mat &src2){
    Mat ft;
    Mat kernel = Mat::ones(2, 2, CV_64FC1);
    kernel = kernel.mul(-1);

    Mat dst1, dst2;
    filter2D(src1, dst1, -1, kernel);
    kernel = kernel.mul(-1);
    filter2D(src2, dst2, -1, kernel);

    ft = dst1 + dst2;
    return ft;
}

bool isInsideImage(int y, int x, Mat &m){
    int width = m.cols;
    int height = m.rows;
    if(x >= 0 && x < width && y >= 0 && y < height) return true;
    else return false;
}

double get_Sum9(Mat &m, int y, int x){
    if(x < 0 || x >= m.cols) return 0;
    if(y < 0 || y >= m.rows) return 0;

    double val = 0.0;
    int tmp = 0;
    if(isInsideImage(y - 1, x - 1, m)){
        ++ tmp;
        val += m.ATD(y - 1, x - 1);
    }
    if(isInsideImage(y - 1, x, m)){
        ++ tmp;
        val += m.ATD(y - 1, x);
    }
    if(isInsideImage(y - 1, x + 1, m)){
        ++ tmp;
        val += m.ATD(y - 1, x + 1);
    }
    if(isInsideImage(y, x - 1, m)){
        ++ tmp;
        val += m.ATD(y, x - 1);
    }
    if(isInsideImage(y, x, m)){
        ++ tmp;
        val += m.ATD(y, x);
    }
    if(isInsideImage(y, x + 1, m)){
        ++ tmp;
        val += m.ATD(y, x + 1);
    }
    if(isInsideImage(y + 1, x - 1, m)){
        ++ tmp;
        val += m.ATD(y + 1, x - 1);
    }
    if(isInsideImage(y + 1, x, m)){
        ++ tmp;
        val += m.ATD(y + 1, x);
    }
    if(isInsideImage(y + 1, x + 1, m)){
        ++ tmp;
        val += m.ATD(y + 1, x + 1);
    }
    if(tmp == 9) return val;
    else return m.ATD(y, x) * 9;
}

Mat get_Sum9_Mat(Mat &m){
    Mat res = Mat::zeros(m.rows, m.cols, CV_64FC1);
    for(int i = 1; i < m.rows - 1; i++){
        for(int j = 1; j < m.cols - 1; j++){
            res.ATD(i, j) = get_Sum9(m, i, j);
        }
    }
    return res;
}

void saveMat(Mat &M, string s){
    s += ".txt";
    FILE *pOut = fopen(s.c_str(), "w+");
    for(int i=0; i<M.rows; i++){
        for(int j=0; j<M.cols; j++){
            fprintf(pOut, "%lf", M.ATD(i, j));
            if(j == M.cols - 1) fprintf(pOut, "\n");
            else fprintf(pOut, " ");
        }
    }
    fclose(pOut);
}

void getLucasKanadeOpticalFlow(Mat &img1, Mat &img2, Mat &u, Mat &v){

    Mat fx = get_fx(img1, img2);
    Mat fy = get_fy(img1, img2);
    Mat ft = get_ft(img1, img2);

    Mat fx2 = fx.mul(fx);
    Mat fy2 = fy.mul(fy);
    Mat fxfy = fx.mul(fy);
    Mat fxft = fx.mul(ft);
    Mat fyft = fy.mul(ft);

    Mat sumfx2 = get_Sum9_Mat(fx2);
    Mat sumfy2 = get_Sum9_Mat(fy2);
    Mat sumfxft = get_Sum9_Mat(fxft);
    Mat sumfxfy = get_Sum9_Mat(fxfy);
    Mat sumfyft = get_Sum9_Mat(fyft);

    Mat tmp = sumfx2.mul(sumfy2) - sumfxfy.mul(sumfxfy);
    u = sumfxfy.mul(sumfyft) - sumfy2.mul(sumfxft);
    v = sumfxft.mul(sumfxfy) - sumfx2.mul(sumfyft);
    divide(u, tmp, u);
    divide(v, tmp, v);

//    saveMat(u, "U");
//    saveMat(v, "V");   
}



int main(){

    Mat img1 = imread("car1.jpg", 0);
    Mat img2 = imread("car2.jpg", 0);
//    Mat img1 = imread("table1.jpg", 0);
//    Mat img2 = imread("table2.jpg", 0);
//    Mat img1 = imread("anim.00.tif", 0);
//    Mat img2 = imread("anim.01.tif", 0);
//    Mat img1 = imread("frame07.png", 0);
//    Mat img2 = imread("frame08.png", 0);


    img1.convertTo(img1, CV_64FC1, 1.0/255, 0);
    img2.convertTo(img2, CV_64FC1, 1.0/255, 0);


    Mat u = Mat::zeros(img1.rows, img1.cols, CV_64FC1);
    Mat v = Mat::zeros(img1.rows, img1.cols, CV_64FC1);


    getLucasKanadeOpticalFlow(img1, img2, u, v);


//    waitKey(0);

    return 0;
}














