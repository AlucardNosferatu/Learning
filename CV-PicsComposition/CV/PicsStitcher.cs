using OpenCvSharp;
using OpenCvSharp.XFeatures2D;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CV
{
    class PicsStitcher
    {
        class four_corners_t
        {
            public Point2f left_top;
            public Point2f left_bottom;
            public Point2f right_top;
            public Point2f right_bottom;
        }
        static Point2d f2d(Point2f fuckPoint)
        {
            Point2d P = new Point2d();
            P.X = fuckPoint.X;
            P.Y = fuckPoint.Y;
            return P;
        }
        static four_corners_t CalcCorners(Mat H, Mat src)
        {
            four_corners_t corners = new four_corners_t();
            double[] v2 = { 0, 0, 1 };
            double[] v1 = new double[3];
            Mat V2 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v2);
            Mat V1 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v1);

            V1 = H * V2;

            corners.left_top.X = (float)(v1[0] / v1[2]);
            corners.left_top.Y = (float)(v1[1] / v1[2]);

            //左下角(0,src.rows,1)
            v2[0] = 0;
            v2[1] = src.Rows;
            v2[2] = 1;
            V2 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v2);
            V1 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v1);
            V1 = H * V2;
            corners.left_bottom.X = (float)(v1[0] / v1[2]);
            corners.left_bottom.Y = (float)(v1[1] / v1[2]);

            //右上角(src.cols,0,1)
            v2[0] = src.Cols;
            v2[1] = 0;
            v2[2] = 1;
            V2 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v2);
            V1 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v1);
            V1 = H * V2;
            corners.right_top.X = (float)(v1[0] / v1[2]);
            corners.right_top.Y = (float)(v1[1] / v1[2]);

            //右下角(src.cols,src.rows,1)
            v2[0] = src.Cols;
            v2[1] = src.Rows;
            v2[2] = 1;
            V2 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v2);
            V1 = new Mat(rows: 3, cols: 1, type: MatType.CV_64FC1, v1);
            V1 = H * V2;
            corners.right_bottom.X = (float)(v1[0] / v1[2]);
            corners.right_bottom.Y = (float)(v1[1] / v1[2]);
            return corners;
        }
        public static Mat StitchPics(Mat left, Mat right)
        {
            KeyPoint[] keypoints1;
            KeyPoint[] keypoints2;
            DMatch[] matched = SURF_Matcher(left, right, out keypoints1, out keypoints2);
            List<Point2d> k1 = new List<Point2d>();
            List<Point2d> k2 = new List<Point2d>();
            for (int i = 0; i < matched.Length; i++)
            {
                k1.Add(f2d(keypoints1[matched[i].QueryIdx].Pt));
                k2.Add(f2d(keypoints2[matched[i].TrainIdx].Pt));
            }
            Mat homo = Cv2.FindHomography(k1, k2, HomographyMethods.Ransac);
            four_corners_t corners = CalcCorners(homo, right);
            Mat imageTransform1 = new Mat();
            Mat imageTransform2 = new Mat();
            Cv2.WarpPerspective(right, imageTransform1, homo, new Size(Math.Max(corners.right_top.X, corners.right_bottom.X), left.Rows));
            int dst_width = imageTransform1.Cols;  //取最右点的长度为拼接图的长度
            int dst_height = left.Rows;
            Mat dst = new Mat(dst_height, dst_width, MatType.CV_8UC3);
            dst.SetTo(0);
            Mat roi1 = new Mat(dst, new Rect(0, 0, imageTransform1.Cols, imageTransform1.Rows));
            Mat roi2 = new Mat(dst, new Rect(0, 0, left.Cols, left.Rows));
            imageTransform1.CopyTo(roi1);
            left.CopyTo(roi2);

            //OptimizeSeam(b, imageTransform1, dst);

            return dst;
        }
        public static Mat OneStepStitcher(Mat left, Mat right)
        {
            Stitcher stitcher = Stitcher.Create(Stitcher.Mode.Scans);
            Mat[] input = { left, right };
            Mat pano = new Mat();
            stitcher.Stitch(input, pano);
            return pano;
        }
        static DMatch[] SURF_Matcher(Mat left, Mat right, out KeyPoint[] keypoints1, out KeyPoint[] keypoints2, double distThres = 0.2)
        {

            SURF surf = SURF.Create(2000, 4, 2, true);

            MatOfFloat descriptors1 = new MatOfFloat();
            MatOfFloat descriptors2 = new MatOfFloat();
            surf.DetectAndCompute(left, null, out keypoints1, descriptors1);
            surf.DetectAndCompute(right, null, out keypoints2, descriptors2);
            BFMatcher matcher = new BFMatcher(NormTypes.L2, true);
            DMatch[] matches = matcher.Match(descriptors1, descriptors2);
            Mat view = new Mat();
            int count = 0;
            int[] shortestPart = new int[matches.Length];
            for (int i = 0; i < matches.Length; i++)
            {
                if (matches[i].Distance <= distThres && count < shortestPart.Length)
                {
                    shortestPart[count] = i;
                    count++;
                }
            }
            DMatch[] newM = new DMatch[count];
            for (int i = 0; i < count; i++)
            {
                newM[i] = matches[shortestPart[i]];
            }
            return newM;

        }
    }
}
