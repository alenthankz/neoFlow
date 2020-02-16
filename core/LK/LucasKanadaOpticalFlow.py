import gaussian_pyramid


class LucasKanade:

    def __init__():


    
    def calculate_flow(self, frame1, frame2):

    




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