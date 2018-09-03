from stegano import Stegano

input_dir = 'imagens'
output_dir = 'output'
file = 'FotoEscura3_crop.png'

content_str = 'Lorem'

stegano_enc = Stegano(input_dir + '/' + file)
stegano_enc.encode(content_str)
stegano_enc.save(output_dir + '/' + file, output_dir + '/diff-' + file)

stegano_dec = Stegano(output_dir + '/' + file)
str_decoded = stegano_dec.decode(len(content_str))
print(str_decoded)